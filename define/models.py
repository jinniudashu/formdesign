from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Q
import uuid
from pypinyin import Style, lazy_pinyin

from formdesign.hsscbase_class import HsscBase, HsscPymBase
from define_icpc.models import Icpc


class HsscFieldBase(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'boolfield_{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


###############################################################################
# 业务字段类型定义
###############################################################################

# 字符字段
class CharacterField(HsscFieldBase):
    CHAR_TYPE = [('CharField', '单行文本'), ('TextField', '多行文本')]
    type = models.CharField(max_length=50, choices=CHAR_TYPE, default='CharField', verbose_name="类型")
    length = models.PositiveSmallIntegerField(default=255, verbose_name="字符长度")
    required = models.BooleanField(default=False, verbose_name="必填")
    default = models.CharField(max_length=255, null=True, blank=True, verbose_name="默认值")
    # component = GenericRelation(to='Component')

    class Meta:
        verbose_name = "字符字段"
        verbose_name_plural = "字符字段"


# 数值字段
class NumberField(HsscFieldBase):
    NUMBER_TYPE = [('IntegerField', '整数'), ('DecimalField', '固定精度小数'), ('FloatField', '浮点数')]
    type = models.CharField(max_length=50, choices=NUMBER_TYPE, default='IntegerField', verbose_name="类型")
    max_digits = models.PositiveSmallIntegerField(default=10, verbose_name="最大位数", null=True, blank=True)
    decimal_places = models.PositiveSmallIntegerField(default=2, verbose_name="小数位数", null=True, blank=True)
    standard_value = models.FloatField(null=True, blank=True, verbose_name="标准值")
    up_limit = models.FloatField(null=True, blank=True, verbose_name="上限")
    down_limit = models.FloatField(null=True, blank=True, verbose_name="下限")
    unit = models.CharField(max_length=50, null=True, blank=True, verbose_name="单位")
    default = models.FloatField(null=True, blank=True, verbose_name="默认值")
    required = models.BooleanField(default=False, verbose_name="必填")

    class Meta:
        verbose_name = "数值字段"
        verbose_name_plural = "数值字段"


# 日期时间字段
class DTField(HsscFieldBase):
    DT_TYPE = [('DateTimeField', '日期时间'), ('DateField', '日期')]
    type = models.CharField(max_length=50, choices=DT_TYPE, default='DateTimeField', verbose_name="类型")
    default_now = models.BooleanField(default=False, verbose_name="默认为当前时间")
    required = models.BooleanField(default=False, verbose_name="必填")

    class Meta:
        verbose_name = "日期字段"
        verbose_name_plural = "日期字段"


# 关联字段基础表
# 内容由DicList和define_operand.ManagedEntity生成内容时自动维护
class RelateFieldModel(HsscBase):
    related_content = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联内容")
    Related_content_type = [('diclist', '基础字典'), ('icpclist', 'ICPC'), ('managedentity', '管理实体')]
    related_content_type = models.CharField(max_length=20, choices=Related_content_type, default=0, verbose_name="关联内容类型")

    class Meta:
        verbose_name = "关联字段基础表"
        verbose_name_plural = "关联字段基础表"

# RelationField关联Model
#     1. 所有字典表
#     2. 所有ICPC表
#     3. 所有业务管理实体基础表

# 关联字段
class RelatedField(HsscFieldBase):
    CHOICE_TYPE = [('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')]
    type = models.CharField(max_length=50, choices=CHOICE_TYPE, default='ChoiceField', verbose_name="类型")
    related_content = models.ForeignKey(RelateFieldModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="关联内容")

    class Meta:
        verbose_name = "关联字段"
        verbose_name_plural = "关联字段"


# 字段列表
class Component(HsscPymBase):
    q  = Q(app_label='define') & (
        Q(model = 'characterfield') | 
        Q(model = 'numberfield') | 
        Q(model = 'dtfield') | 
        Q(model = 'relatedfield')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=q , null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "业务字段汇总"
        verbose_name_plural = verbose_name
        ordering = ['id']

# 组件
class ComponentsGroup(HsscPymBase):
    components = models.ManyToManyField(Component, verbose_name="字段")

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'relatedfield_{"_".join(lazy_pinyin(self.label)).lower()}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "组件"
        verbose_name_plural = "组件"


# 如果保存字段表，则更新Component表
@receiver(post_save, sender=CharacterField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=NumberField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=DTField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=RelatedField, weak=True, dispatch_uid=None)
def fields_post_save_handler(sender, instance, created, **kwargs):
    if instance.name_icpc:
        component_name = instance.name_icpc.icpc_code
        component_label = instance.name_icpc.iname
    else:
        component_name = instance.name
        component_label = instance.label
    content_type = ContentType.objects.get(app_label='define', model=sender.__name__.lower())
    print(content_type, ':', instance.name)
    if created:
        Component.objects.create(
            content_type = content_type, 
            object_id = instance.id, 
            name = component_name, 
            label = component_label,
            hssc_id = instance.hssc_id
        )
    else:
        Component.objects.filter(hssc_id=instance.hssc_id).update(
            name = component_name,
            label = instance.label, 
            content_type = content_type,
            object_id = instance.id,
        )

@receiver(post_delete, sender=CharacterField, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=NumberField, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=DTField, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=RelatedField, weak=True, dispatch_uid=None)
def fields_post_delete_handler(sender, instance, **kwargs):
    Component.objects.filter(hssc_id=instance.hssc_id).delete()


# 字典列表
class DicList(HsscPymBase):
    class Meta:
        verbose_name = "自定义关联字典"
        verbose_name_plural = verbose_name


# 字典明细
class DicDetail(HsscPymBase):
    diclist = models.ForeignKey(DicList, on_delete=models.CASCADE, blank=True, null=True, verbose_name="字典")
    value = models.CharField(max_length=255, verbose_name="值")
    icpc = models.ForeignKey(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "业务字典明细"
        verbose_name_plural = verbose_name


# Icpc字典列表
class IcpcList(HsscPymBase):
    app_name = models.CharField(max_length=100, verbose_name="所属app名", null=True, blank=True)
    model_name = models.CharField(max_length=100, verbose_name="模型名", null=True, blank=True)

    class Meta:
        verbose_name = "ICPC字典列表"
        verbose_name_plural = verbose_name

# Sync Create and update RelateFieldModel
@receiver(post_save, sender=DicList, weak=True, dispatch_uid=None)
@receiver(post_save, sender=IcpcList, weak=True, dispatch_uid=None)
def relate_field_model_post_save_handler(sender, instance, created, **kwargs):
    # if sender==DicList:
    #     _related_content = instance.name.capitalize()
    # elif sender==IcpcList:
    #     _related_content = instance.model_name
    if created:
        RelateFieldModel.objects.create(
            name=instance.name,
            label=instance.label,
            related_content=instance.name.capitalize(),
            related_content_type=sender._meta.model_name,
            hssc_id = instance.hssc_id
        )
    else:
        RelateFieldModel.objects.filter(hssc_id=instance.hssc_id).update(
            name=instance.name,
            label=instance.label,
            related_content=instance.name.capitalize(),
            related_content_type=sender._meta.model_name,
        )


# 角色表
class Role(HsscPymBase):
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="角色描述")

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        ordering = ['id']
