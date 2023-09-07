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
    label = models.CharField(max_length=63, null=True, verbose_name="名称")
    name = models.CharField(max_length=63, blank=True, null=True, verbose_name="name")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
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

    class Meta:
        verbose_name = "数值字段"
        verbose_name_plural = "数值字段"


# 日期时间字段
class DTField(HsscFieldBase):
    DT_TYPE = [('DateTimeField', '日期时间'), ('DateField', '日期')]
    type = models.CharField(max_length=50, choices=DT_TYPE, default='DateTimeField', verbose_name="类型")
    default_now = models.BooleanField(default=False, verbose_name="默认为当前时间")

    class Meta:
        verbose_name = "日期字段"
        verbose_name_plural = "日期字段"


# 关联字段基础表
# 内容由DicList, ICPC, define_operand.ManagedEntity, define_operand.CoreModel生成内容时自动维护
class RelateFieldModel(HsscBase):
    related_content = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联内容")
    Related_content_type = [('dictionaries', '基础字典'), ('icpc', 'ICPC'), ('service', '管理实体'), ('core', '内核')]  # 关联内容所属Hssc.app
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
    related_content = models.ForeignKey(RelateFieldModel, on_delete=models.CASCADE, null=True, verbose_name="关联内容")

    class Meta:
        verbose_name = "关联字段"
        verbose_name_plural = "关联字段"


# 上传文件字段
class FileField(HsscFieldBase):
    FILE_TYPE = [('ImageField', '图片'), ('FileField', '文件')]
    type = models.CharField(max_length=50, choices=FILE_TYPE, default='ImageField', verbose_name="类型")

    class Meta:
        verbose_name = "文件字段"
        verbose_name_plural = "文件字段"

# 系统字段
class SystemReservedField(HsscFieldBase):
    FIELD_TYPE = [('charge_staff', '责任人'), ('operator', '作业人员'), ('scheduled_time', '计划执行时间'), ('duration', '时长'), ('frequency', '频次')]
    type = models.CharField(max_length=50, choices=FIELD_TYPE, default='ImageField', verbose_name="类型")

    class Meta:
        verbose_name = "系统字段"
        verbose_name_plural = "系统字段"

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


# 如果保存字段表，则更新Component表
@receiver(post_save, sender=CharacterField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=NumberField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=DTField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=RelatedField, weak=True, dispatch_uid=None)
@receiver(post_save, sender=FileField, weak=True, dispatch_uid=None)
def fields_post_save_handler(sender, instance, created, **kwargs):
    if instance.name_icpc:
        component_label = instance.name_icpc.iname
    else:
        component_label = instance.label
    content_type = ContentType.objects.get(app_label='define', model=sender.__name__.lower())
    print(content_type, ':', instance.name)
    if created:
        Component.objects.create(
            content_type = content_type, 
            object_id = instance.id, 
            name = instance.name, 
            label = component_label,
            hssc_id = instance.hssc_id
        )
    else:
        Component.objects.filter(hssc_id=instance.hssc_id).update(
            name = instance.name,
            label = instance.label, 
            content_type = content_type,
            object_id = instance.id,
        )

@receiver(post_delete, sender=CharacterField, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=NumberField, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=DTField, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=RelatedField, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=FileField, weak=True, dispatch_uid=None)
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
    if sender==DicList:
        app_name = 'dictionaries'
    elif sender==IcpcList:
        app_name = 'icpc'
    if created:
        RelateFieldModel.objects.create(
            name=instance.name,
            label=instance.label,
            related_content=instance.name.capitalize(),
            related_content_type=app_name,
            hssc_id = instance.hssc_id
        )
    else:
        RelateFieldModel.objects.filter(hssc_id=instance.hssc_id).update(
            name=instance.name,
            label=instance.label,
            related_content=instance.name.capitalize(),
            related_content_type=app_name,
        )


# 角色表
class Role(HsscPymBase):
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="岗位描述")

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "业务岗位"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 药品基本信息表
class Medicine(HsscPymBase):
    yp_code = models.CharField(max_length=10, null=True, verbose_name="药品编码")
    specification = models.CharField(max_length=100, null=True, verbose_name="规格")
    cf_measure = models.CharField(max_length=30, null=True, verbose_name="处方剂量单位")
    dosage = models.CharField(max_length=60, null=True, verbose_name="常用剂量")
    usage = models.CharField(max_length=60, null=True, verbose_name="用药途径")
    fypc = models.CharField(max_length=255, null=True, verbose_name="用药频次")
    fyzysxhbz = models.CharField(max_length=255, null=True, verbose_name="用药备注")
    type = models.CharField(max_length=40, null=True, verbose_name="药剂类型")
    yp_sort = models.CharField(max_length=60, null=True, verbose_name="药品分类")
    ypglsx = models.CharField(max_length=60, null=True, verbose_name="药品管理属性")
    ypty_name = models.CharField(max_length=200, null=True, verbose_name="药品通用名称")
    gjjbyp = models.CharField(max_length=100, null=True, verbose_name="国家基本药品目录名称")
    ybypbm = models.CharField(max_length=100, null=True, verbose_name="医保药品目录对应药品编码")
    ybyplb = models.CharField(max_length=2, null=True, verbose_name="医保报销类别")
    syz = models.CharField(max_length=255, null=True, verbose_name="适应症")
    bsyz = models.CharField(max_length=255, null=True, verbose_name="不适应症")
    blfy = models.CharField(max_length=255, null=True, verbose_name="不良反应")
    mz_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="门诊参考单价")

    class Meta:
        verbose_name = "药品基本信息表"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.label


# 药品基本信息导入表
class MedicineImport(models.Model):
    YPCode = models.CharField(max_length=10, verbose_name="药品编码")
    PYM = models.CharField(max_length=100, null=True, verbose_name="拼音码")
    YPName = models.CharField(max_length=200, null=True, verbose_name="药品名称")
    Specification = models.CharField(max_length=100, null=True, verbose_name="规格")
    CFMeasure = models.CharField(max_length=30, null=True, verbose_name="处方剂量单位")
    Dosage = models.CharField(max_length=60, null=True, verbose_name="常用剂量")
    Usage = models.CharField(max_length=60, null=True, verbose_name="用药途径")
    Frequency = models.CharField(max_length=255, null=True, verbose_name="用药频次")
    Note = models.CharField(max_length=255, null=True, verbose_name="用药备注")
    Type = models.CharField(max_length=40, null=True, verbose_name="药剂类型")
    YPClass = models.CharField(max_length=60, null=True, verbose_name="药品分类")
    DrugAdministrationAttributes = models.CharField(max_length=60, null=True, verbose_name="药品管理属性")
    YptyName = models.CharField(max_length=200, null=True, verbose_name="药品通用名称")
    Gjjbyp = models.CharField(max_length=100, null=True, verbose_name="国家基本药品目录名称")
    Ybypbm = models.CharField(max_length=100, null=True, verbose_name="医保药品目录对应药品编码")
    Ybyplb = models.CharField(max_length=2, null=True, verbose_name="医保报销类别")
    Indications = models.CharField(max_length=255, null=True, verbose_name="适应症")
    Incompatibility = models.CharField(max_length=255, null=True, verbose_name="不适应症")
    AdverseReactions = models.CharField(max_length=255, null=True, verbose_name="不良反应")

    class Meta:
        verbose_name = "药品基本信息导入表"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.YPName


# 从MedicineImport导入药品信息至Medicine
def medicine_import():
    # 字段映射
    field_map = {
        'label' : 'YPName',
        'yp_code' : 'YPCode',  # "药品编码"
        'specification' : 'Specification',  # "规格"
        'cf_measure' : 'CFMeasure',  # "处方剂量单位"
        'dosage' : 'Dosage',  # "常用剂量"
        'usage' : 'Usage',  # "用药途径"
        'fypc' : 'Frequency',  # "用药频次"
        'fyzysxhbz' : 'Note',  # "用药备注"
        'type' : 'Type',  # "药剂类型"
        'yp_sort' : 'YPClass',  # "药品分类"
        'ypglsx' : 'DrugAdministrationAttributes',  # "药品管理属性"
        'ypty_name' : 'YptyName',  # "药品通用名称"
        'gjjbyp' : 'Gjjbyp',  # "国家基本药品目录名称"
        'ybypbm' : 'Ybypbm',  # "医保药品目录对应药品编码"
        'ybyplb' : 'Ybyplb',  # "医保报销类别"
        'syz' : 'Indications',  # "适应症"
        'bsyz' : 'Incompatibility',  # "不适应症"
        'blfy' : 'AdverseReactions',  # "不良反应"
    }

    # 逐条导入MedicineImport的记录至Medicine
    for medicine_import in MedicineImport.objects.all():
        medicine = Medicine()
        for field in medicine._meta.fields:
            if field.name in field_map:
                # 从MedicineImport中取出对应字段的值，去除首尾空格
                value = getattr(medicine_import, field_map.get(field.name))
                stripped_value = value.strip()
                # 将值赋给Medicine
                setattr(medicine, field.name, stripped_value)
        medicine.save()
