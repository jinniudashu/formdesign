from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Q
import json

from pypinyin import lazy_pinyin

from define.models import Component
from define_dict.models import ManagedEntity


# 基础表单定义
class BaseModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, unique=True, verbose_name="表单名称")
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    components = models.ManyToManyField(Component, verbose_name="组件清单")
    managed_entity = models.ManyToManyField(ManagedEntity, verbose_name="关联实体", blank=True)
    is_base_infomation = models.BooleanField(default=False, verbose_name="基础信息表")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "基础表单"
        verbose_name_plural = "基础表单"
        ordering = ['id']


# 基础视图定义
class BaseForm(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, unique=True, verbose_name="视图名称")
    basemodel = models.ForeignKey(BaseModel, on_delete=models.CASCADE, verbose_name="基础表单")
    is_inquiry = models.BooleanField(default=False, verbose_name="仅用于查询")
    FORM_STYLE = [('detail', '详情'),('list', '列表')]
    style = models.CharField(max_length=50, choices=FORM_STYLE, default='detail', verbose_name='风格')
    components = models.ManyToManyField(Component, verbose_name="组件清单")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="视图元数据")
    # q = Q(BaseModel.objects.get(id=basemodel).components.all())

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "基础视图"
        verbose_name_plural = "基础视图"
        ordering = ['id']


# 组合视图定义
class CombineForm(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, unique=True, verbose_name="表单名称")
    forms = models.ManyToManyField('self', blank=True, verbose_name="可组合的视图")
    is_base = models.BooleanField(default=False, verbose_name="基础视图")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, blank=True, verbose_name="实体类型")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="视图元数据")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "组合视图"
        verbose_name_plural = "组合视图"
        ordering = ['id']


@receiver(m2m_changed, sender=BaseModel.components.through)
# BaseModel变更components字段，更新相应BaseForm的components字段
def basemodel_m2m_changed_handler(sender, instance, action, **kwargs):
    for baseform in instance.baseform_set.all():
        baseform.components.add(*instance.components.all())
        baseform.save()


@receiver(m2m_changed, sender=BaseForm.components.through)
def baseform_m2m_changed_handler(sender, instance, action, **kwargs):
        # 根据components的变更生成字段记录
        # fields = list(instance.components.values_list('name', flat=True))
        fields = []
        for component in instance.components.all():
            field = {}
            field['name'] = component.name
            field['label'] = component.label
            _type = component.content_object._meta.object_name
            if _type == 'CharacterField':
                field['type'] = 'string'
            elif _type == 'BoolField':
                field['type'] = 'boolean'
            elif _type == 'NumberField':
                field['type'] = 'number'
            elif _type == 'DTField':
                field['type'] = 'datetime'
            elif _type == 'ChoiceField' or _type == 'RelatedField':
                # 获取关联字段的模型???
                print('component', component)
                field['type'] = 'dict'
                field['dict_name'] = component.content_object.related_content.related_content
            fields.append(field)

        meta_data = {}
        meta_data['name'] = instance.name
        meta_data['label'] = instance.label
        if instance.is_inquiry:
            meta_data['mutate_or_inquiry'] = 'inquiry'
        else:
            meta_data['mutate_or_inquiry'] = 'mutate'
        meta_data['style'] = instance.style
        meta_data['basemodel'] = instance.basemodel.name
        meta_data['fields'] = fields
        
        # 更新基础视图的meta_data，类型为dict
        instance.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
        instance.save()

        # 更新组合视图的meta_data字段, 类型为list
        combine_form_meta_data = json.dumps([meta_data], ensure_ascii=False, indent=4)
        CombineForm.objects.filter(name=instance.name).update(meta_data=combine_form_meta_data)


@receiver(m2m_changed, sender=CombineForm.forms.through)
def combineform_m2m_changed_handler(sender, instance, action, **kwargs):
    # 合成每个组合视图的meta_data
    meta_data = []
    for item in instance.forms.all():
        _meta_data = json.loads(item.meta_data)
        if isinstance(_meta_data, list):  # forms中可能包含CombineForm，这时item.meta_data是数组，需要先解包
            for i, v in enumerate(_meta_data):
                meta_data.append(v)
        else:
            meta_data.append(_meta_data)
    instance.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
    instance.save()


# 收到表单保存信号
@receiver(post_save, sender=BaseModel)
# 生成BaseModel时，自动生成BaseForm
def basemodel_post_save_handler(sender, instance, created, **kwargs):
    if created:
        BaseForm.objects.create(
            name = f'{instance.name}_baseform', 
            label = instance.label, 
            basemodel = instance,
            is_inquiry = False,
            style = 'detail',
            # components字段是m2m, 由basemodel_m2m_changed_handler处理
        )


@receiver(post_save, sender=BaseForm)
# 生成BaseForm时，自动生成CombineForm
def baseform_post_save_handler(sender, instance, created, **kwargs):
    if created:
        c = CombineForm.objects.create(
            name=instance.name,
            label=instance.label,
            is_base=True,
        )
        c.forms.add(c)
