from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from pypinyin import lazy_pinyin

from django.dispatch import receiver
from django.db.models.signals import post_save

from define_dict.models import DicList, ManagedEntity


# 关联字段模型
# 内容由DicList和ManagedEntity生成内容时自动维护
class RelateFieldModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="关联模型名称")
    related_content = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联内容")
    display_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="显示字段")
    related_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联字段")
    q = Q(app_label='define_dict' ) & Q(model = 'diclist') | Q(app_label='define_form') & Q(model = 'managedentity')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=q, null=True, blank=True, verbose_name="关联基本信息")
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "关联字段基础表"
        verbose_name_plural = "关联字段基础表"

# RelationField关联Model
#     1. 所有字典表
#     2. 所有ICPC表
#     3. 角色基本信息表
#     4. 职员基本信息表?
#     5. 个人基本信息表?
#     6. 药品基本信息表?


###############################################################################
# 业务字段类型定义
###############################################################################

# 布尔字段
class BoolField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单字段")
    CHOICES_TYPE = [('0', '是, 否'), ('1', '未知, 是, 否')]
    type = models.CharField(max_length=100, choices=CHOICES_TYPE , default='1', verbose_name="可选值")
    required = models.BooleanField(default=False, verbose_name="必填")
    DEFAULT_VALUE = [('0', '未知'), ('1', '是'), ('2', '否')]
    default = models.CharField(max_length=10, choices=DEFAULT_VALUE, default='0', null=True, blank=True, verbose_name="默认值")

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'boolfield_{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "是否字段"
        verbose_name_plural = "是否字段"

# 字符字段
class CharacterField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单字段")
    CHAR_TYPE = [('CharField', '单行文本'), ('TextField', '多行文本')]
    type = models.CharField(max_length=50, choices=CHAR_TYPE, default='CharField', verbose_name="类型")
    length = models.PositiveSmallIntegerField(default=255, verbose_name="字符长度")
    required = models.BooleanField(default=False, verbose_name="必填")
    default = models.CharField(max_length=255, null=True, blank=True, verbose_name="默认值")
    # component = GenericRelation(to='Component')

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'characterfield_{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "字符字段"
        verbose_name_plural = "字符字段"


# 数值字段
class NumberField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单字段")
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

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'numberfield_{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "数值字段"
        verbose_name_plural = "数值字段"


# 日期时间字段
class DTField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单字段")
    DT_TYPE = [('DateTimeField', '日期时间'), ('DateField', '日期')]
    type = models.CharField(max_length=50, choices=DT_TYPE, default='DateTimeField', verbose_name="类型")
    default_now = models.BooleanField(default=False, verbose_name="默认为当前时间")
    required = models.BooleanField(default=False, verbose_name="必填")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'datetimefield_{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "日期字段"
        verbose_name_plural = "日期字段"


# 选择字段
class ChoiceField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单字段")
    CHOICE_TYPE = [('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')]
    type = models.CharField(max_length=50, choices=CHOICE_TYPE, default='ChoiceField', verbose_name="类型")
    options = models.TextField(max_length=1024, null=True, blank=True, verbose_name="选项", help_text="每行一个选项, 最多100个")
    default_first = models.BooleanField(default=False, verbose_name="默认选第一个")
    required = models.BooleanField(default=False, verbose_name="必填")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'choicefield_{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "选择字段"
        verbose_name_plural = "选择字段"


# 关联字段
class RelatedField(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, unique=True, verbose_name="表单字段")
    CHOICE_TYPE = [('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')]
    type = models.CharField(max_length=50, choices=CHOICE_TYPE, default='ChoiceField', verbose_name="类型")
    # related_content是弃用的旧字段，待完成升级后清理
    # related_content = models.ForeignKey(DicList, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联内容-旧版")
    related_content = models.ForeignKey(RelateFieldModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="关联内容")
    # related_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联字段")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'relatedfield_{"_".join(lazy_pinyin(self.label)).lower()}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "关联字段"
        verbose_name_plural = "关联字段"

# Updated items:
# 服务角色
# 病名-评估和诊断
# 症状-症状和问题

# 计算字段
class ComputeField(models.Model):
    pass


# 字段列表
class Component(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单字段", null=True, blank=True)

    q  = Q(app_label='define') & (
        Q(model = 'boolfield') | 
        Q(model = 'characterfield') | 
        Q(model = 'numberfield') | 
        Q(model = 'dtfield') | 
        Q(model = 'choicefield') | 
        Q(model = 'relatedfield') | 
        Q(model = 'computefield')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=q , null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "表单字段汇总"
        verbose_name_plural = "表单字段汇总"
        ordering = ['id']


# 如果保存字段表，则更新Component表
@receiver(post_save, sender=BoolField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=CharacterField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=NumberField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=DTField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=ChoiceField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=RelatedField, weak=True, dispatch_uid=None)
def fields_post_save_handler(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get(app_label='define', model=sender.__name__.lower())
    print(content_type, ':', instance.name)
    if created:
        Component.objects.create(
            content_type = content_type, 
            object_id = instance.id, 
            name = instance.name, 
            label = instance.label, 
        )
    else:
        Component.objects.filter(name=instance.name).update(
            content_type = content_type,
            object_id = instance.id,
            label = instance.label, 
        )
        

# Sync Create and update RelateFieldModel
@receiver(post_save, sender=DicList, weak=True, dispatch_uid=None)
@receiver(post_save, sender=ManagedEntity, weak=True, dispatch_uid=None)
def relate_field_model_post_save_handler(sender, instance, created, **kwargs):
    if sender==DicList:
        _app='define_dict'
        _model='diclist'
        related_content=instance.name.capitalize()
        display_field='value'
        related_field='id'
    elif sender==ManagedEntity:
        _app='define'
        _model='managedentity'
        related_content=instance.model_name
        display_field=instance.display_field
        related_field=instance.related_field

    content_type = ContentType.objects.get(app_label=_app, model=_model)
    print(sender, instance)

    if created:
        RelateFieldModel.objects.create(
            name=instance.name,
            label=instance.label,
            related_content=related_content,
            display_field=display_field,
            related_field=related_field,
            content_type = content_type, 
            object_id = instance.id, 
        )
    else:
        RelateFieldModel.objects.filter(name=instance.name).update(
            label=instance.label,
            related_content=related_content,
            display_field=display_field,
            related_field=related_field,
            content_type = content_type, 
            object_id = instance.id, 
        )
