from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Q
import json
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from pypinyin import lazy_pinyin

from define_icpc.models import Icpc
from define.models import Component, ComponentsGroup
from define_dict.models import ManagedEntity


# 业务表单定义
class BuessinessForm(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=100, unique=True, verbose_name="表单名称")
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="描述")
    components = models.ManyToManyField(Component, blank=True, verbose_name="字段")
    components_groups = models.ManyToManyField(ComponentsGroup, blank=True, verbose_name="组件")
    managed_entity = models.ManyToManyField(ManagedEntity, through='EntityFormShip', null=True, blank=True, verbose_name="隶属实体")
    # is_base_infomation = models.BooleanField(default=False, verbose_name="基本信息表")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="元数据")
    buessiness_form_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="业务表单ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.buessiness_form_id is None:
            self.buessiness_form_id = uuid.uuid1()
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name


# 实体和表单关系表
class EntityFormShip(models.Model):
    entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, verbose_name="隶属实体")
    form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="业务表单")
    is_base_infomation = models.BooleanField(default=False, verbose_name="基本信息表")
    relation_field = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name="关联字段")
    entity_form_ship_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="实体表单关系ID")

    def __str__(self):
        return str(self.entity) + '--' + str(self.form)

    def save(self, *args, **kwargs):
        if self.entity_form_ship_id is None:
            self.entity_form_ship_id = uuid.uuid1()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '实体和表单关系'
        verbose_name_plural = verbose_name


# 基础表单定义
class BaseModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=100, unique=True, verbose_name="表单名称")
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    components = models.ManyToManyField(Component, verbose_name="字段")
    managed_entity = models.ManyToManyField(ManagedEntity, verbose_name="关联实体", blank=True)
    is_base_infomation = models.BooleanField(default=False, verbose_name="基础信息表")
    basemodel_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="基础表单ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.basemodel_id is None:
            self.basemodel_id = uuid.uuid1()
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "基础表单"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 基础视图定义
class BaseForm(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, unique=True, verbose_name="视图名称")
    basemodel = models.ForeignKey(BaseModel, on_delete=models.CASCADE, verbose_name="基础表单")
    is_inquiry = models.BooleanField(default=False, verbose_name="仅用于查询")
    FORM_STYLE = [('detail', '详情'),('list', '列表')]
    style = models.CharField(max_length=50, choices=FORM_STYLE, default='detail', verbose_name='风格')
    components = models.ManyToManyField(Component, verbose_name="字段")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="视图元数据")
    baseform_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="基础视图ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.baseform_id is None:
            self.baseform_id = uuid.uuid1()
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "基础视图"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 组合视图定义
class CombineForm(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=100, unique=True, verbose_name="表单名称")
    forms = models.ManyToManyField(BaseForm, blank=True, verbose_name="可用视图")
    is_base = models.BooleanField(default=False, verbose_name="基础视图")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, blank=True, verbose_name="实体类型")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="视图元数据")
    combineform_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="组合视图ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.combineform_id is None:
            self.combineform_id = uuid.uuid1()
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "组合视图"
        verbose_name_plural = verbose_name
        ordering = ['id']


@receiver(m2m_changed, sender=BaseModel.components.through)
# BaseModel变更components字段，更新相应BaseForm的components字段
def basemodel_m2m_changed_handler(sender, instance, action, **kwargs):
    for baseform in instance.baseform_set.all():
        baseform.components.set(instance.components.all())


# 生成CombineForm的meta_data
def generate_combineform_meta_data(instance):
    meta_data = []
    for baseform in instance.forms.all():
        _meta_data = json.loads(baseform.meta_data)
        meta_data.append(_meta_data)
    instance.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
    instance.save()


@receiver(m2m_changed, sender=BaseForm.components.through)
def baseform_m2m_changed_handler(sender, instance, action, **kwargs):
        # 根据新的components字段，更新meta_data字段
        meta_data = {}
        meta_data['name'] = instance.name
        meta_data['label'] = instance.label

        # 根据components的变更生成字段记录
        fields = []
        for component in instance.components.all():
            field = {}
            field['name'] = component.name
            field['label'] = component.label
            field['field_id'] = component.field_id
            _type = component.content_object._meta.object_name
            if _type == 'CharacterField':
                field['type'] = 'string'
            elif _type == 'BoolField':
                field['type'] = 'boolean'
            elif _type == 'NumberField':
                field['type'] = 'number'
            elif _type == 'DTField':
                field['type'] = 'datetime'
            elif _type == 'RelatedField':
                field['type'] = component.content_object.related_content.related_content  # 关联表的Model名称
                hssc_app_label = component.content_object.related_content.content_type.model
                if hssc_app_label == 'diclist':  # 字典表
                    hssc_app_label = 'dictionaries'  # 指向hssc.dictionaries
                elif hssc_app_label == 'managedentity':  # 实体表
                    hssc_app_label = component.content_object.related_content.content_object.app_name  # 指向hssc.app_name
                field['app_label'] = hssc_app_label
            fields.append(field)
        meta_data['fields'] = fields

        if instance.is_inquiry:
            meta_data['mutate_or_inquiry'] = 'inquiry'
        else:
            meta_data['mutate_or_inquiry'] = 'mutate'
        
        meta_data['style'] = instance.style
        meta_data['basemodel'] = instance.basemodel.name
        meta_data['baseform_id'] = str(instance.baseform_id)

        # 更新meta_data，类型为dict
        instance.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
        instance.save()

        # 更新相应CombineForm的meta_data字段
        for combineform in instance.combineform_set.all():
            generate_combineform_meta_data(combineform)


# 重新生成组合视图的meta_data
@receiver(m2m_changed, sender=CombineForm)
def combineform_m2m_changed_handler(sender, instance, action, **kwargs):
    generate_combineform_meta_data(instance)


# # old_restore_design时恢复使用。使用restore_design时，注释掉不使用
# # 生成BaseModel时，自动生成BaseForm
# @receiver(post_save, sender=BaseModel)
# def basemodel_post_save_handler(sender, instance, created, **kwargs):
#     if created:
#         BaseForm.objects.create(
#             name = f'{instance.name}_baseform', 
#             label = instance.label, 
#             basemodel = instance,
#             is_inquiry = False,
#             style = 'detail',
#             # components字段是m2m, 由basemodel_m2m_changed_handler处理
#         )

# # old_restore_design时恢复使用。使用restore_design时，注释掉不使用
# @receiver(post_save, sender=BaseForm)
# # 生成BaseForm时，自动生成CombineForm
# def baseform_post_save_handler(sender, instance, created, **kwargs):
#     if created:
#         c = CombineForm.objects.create(
#             name=instance.name,
#             label=instance.label,
#             is_base=True,
#         )
#         c.forms.add(instance)
