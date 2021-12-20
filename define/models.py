from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from time import time
from django.db.models.aggregates import Avg

from pypinyin import lazy_pinyin

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed


###############################################################################
# 字段定义
###############################################################################


# 布尔字段
class BoolField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    CHOICES_TYPE = [('0', '是, 否'), ('1', '未知, 是, 否')]
    type = models.CharField(max_length=100, choices=CHOICES_TYPE , default='0', verbose_name="可选值")
    required = models.BooleanField(default=False, verbose_name="必填")
    DEFAULT_VALUE = [('0', '是'), ('1', '否'), ('2', '未知')]
    default = models.CharField(max_length=10, choices=DEFAULT_VALUE, null=True, blank=True, verbose_name="默认值")

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
    label = models.CharField(max_length=100, verbose_name="组件名称")
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
    label = models.CharField(max_length=100, verbose_name="组件名称")
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
    label = models.CharField(max_length=100, verbose_name="组件名称")
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
    label = models.CharField(max_length=100, verbose_name="组件名称")
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


# 字典列表
class DicList(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="字典表名")
    label = models.CharField(max_length=100, verbose_name="字典名称")
    related_field = models.CharField(max_length=100, verbose_name="关联字段")
    content = models.TextField(max_length=1024, null=True, blank=True, verbose_name="字典内容")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "字典列表"
        verbose_name_plural = "字典列表"


# 关联字段
class RelatedField(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称")
    CHOICE_TYPE = [('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')]
    type = models.CharField(max_length=50, choices=CHOICE_TYPE, default='ChoiceField', verbose_name="类型")
    related_content = models.ForeignKey(DicList, on_delete=models.CASCADE, verbose_name="关联内容")
    related_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联字段")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'relatedfield_{"_".join(lazy_pinyin(self.label)).lower()}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "关联字段"
        verbose_name_plural = "关联字段"


# 计算字段
class ComputeField(models.Model):
    pass


# 字段字典
class Component(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="组件名称", null=True, blank=True)

    q = Q(app_label='define') & (
        Q(model = 'characterfield') | 
        Q(model = 'numberfield') | 
        Q(model = 'dtfield') | 
        Q(model = 'choicefield') | 
        Q(model = 'relatedfield') | 
        Q(model = 'computefield')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=q, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "字段字典"
        verbose_name_plural = "字段字典"
        ordering = ['id']


# 基础表单定义
class BaseModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, verbose_name="表单名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    components = models.ManyToManyField(Component, verbose_name="组件清单")

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
    label = models.CharField(max_length=100, null=True, blank=True, verbose_name="视图名称")
    basemodel = models.ForeignKey(BaseModel, on_delete=models.CASCADE, verbose_name="基础表单")
    is_inquiry = models.BooleanField(default=False, verbose_name="仅用于查询")
    FORM_STYLE = [('detail', '详情'),('list', '列表')]
    style = models.CharField(max_length=50, choices=FORM_STYLE, default='detail', verbose_name='风格')
    display_fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="表单字段")
    # q = Q(BaseModel.objects.get(id=basemodel).components.all())
    components = models.ManyToManyField(Component, verbose_name="组件清单")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "基础视图"
        verbose_name_plural = "基础视图"
        ordering = ['id']


# 作业界面定义
class OperandView(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="name")
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="表单名称")
    AXIS_TYPE = [
        ('customer', '客户'),
        ('staff', '员工'),
        ('medicine', '药品'),
        ('device', '设备'),
    ]
    axis_field = models.CharField(max_length=255, choices=AXIS_TYPE, default='customer', verbose_name="业务主键")
    inquire_forms = models.ManyToManyField(BaseForm, limit_choices_to={'is_inquiry': True}, related_name="inquire_forms", blank=True, verbose_name="查询视图")
    mutate_forms = models.ManyToManyField(BaseForm, limit_choices_to={'is_inquiry': False}, related_name="mutate_forms", verbose_name="变更视图")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业界面"
        verbose_name_plural = "作业界面"
        ordering = ['id']


# 源代码库
class SourceCode(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="版本")
    label = models.CharField(max_length=255, verbose_name="版本名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    code = models.TextField(verbose_name="源代码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  

    def __str__(self):
        return str(self.create_time)

    class Meta:
        verbose_name = "源代码"
        verbose_name_plural = "源代码"
        ordering = ['id']


# BaseModel变更components字段，更新相应BaseForm的components字段
@receiver(m2m_changed, sender=BaseModel.components.through)
def basemodel_m2m_changed_handler(sender, instance, action, **kwargs):
    for baseform in instance.baseform_set.all():
        baseform.components.add(*instance.components.all())
        baseform.save()


# 收到表单保存信号
@receiver(post_save, sender=None, weak=True, dispatch_uid=None)
def form_post_save_handler(sender, instance, created, **kwargs):

    # 如果创建的是BaseModel，则同步创建BaseForm表
    if sender == BaseModel and created:
        BaseForm.objects.create(
            name = f'{instance.name}_baseform', 
            label = instance.label, 
            basemodel = instance,
            is_inquiry = False,
            style = 'detail',
            # components字段是m2m, 由basemodel_m2m_changed_handler处理
        )


    # 如果保存字段表，则更新Component表
    if sender in [BoolField, CharacterField, NumberField, DTField, ChoiceField, RelatedField]:
        charfield_type = ContentType.objects.get(app_label='define', model=sender.__name__.lower())
        if created:
            print(charfield_type, ':', instance.name)
            Component.objects.create(
                content_type = charfield_type, 
                object_id = instance.id, 
                name = instance.name, 
                label = instance.label, 
            )
        else:
            Component.objects.filter(content_type=charfield_type, object_id=instance.id).update(
                name = instance.name, 
                label = instance.label, 
            )

