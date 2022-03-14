from django.db import models
from django.forms.models import model_to_dict
import uuid
from pypinyin import Style, lazy_pinyin

icpc_list=[
	{'name': 'Icpc1_register_logins', 'label': '注册登录（行政管理）', 'url': 'icpc-1-s'},  # 28
	{'name': 'Icpc2_reservation_investigations', 'label': '预约咨询调查（行政管理）', 'url': 'icpc-2-s'},  # 19
	{'name': 'Icpc3_symptoms_and_problems', 'label': '症状和问题', 'url': 'icpc-3-s'},  # 1233
	{'name': 'Icpc4_physical_examination_and_tests', 'label': '体格和其他检查', 'url': 'icpc-4-s'},  # 241
	{'name': 'Icpc5_evaluation_and_diagnoses', 'label': '评估和诊断', 'url': 'icpc-5-s'},  # 4488
	{'name': 'Icpc6_prescribe_medicines', 'label': '开药', 'url': 'icpc-6-s'},  # 4
	{'name': 'Icpc7_treatments', 'label': '治疗', 'url': 'icpc-7-s'},  # 11
	{'name': 'Icpc8_other_health_interventions', 'label': '其他健康干预', 'url': 'icpc-8-s'},  # 13
	{'name': 'Icpc9_referral_consultations', 'label': '转诊会诊', 'url': 'icpc-9-s'},  # 8
	{'name': 'Icpc10_test_results_and_statistics', 'label': '检查结果和统计', 'url': 'icpc-10-test-results-and-statistics'},  # 5
]


# ICPC基类
class IcpcBase(models.Model):
    icpc_code = models.CharField(max_length=5, unique=True, blank=True, null=True, verbose_name="icpc码")
    icode = models.CharField(max_length=3, blank=True, null=True, verbose_name="分类码")
    iname = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    iename = models.CharField(max_length=255, blank=True, null=True, verbose_name="English Name")
    include = models.CharField(max_length=1024, blank=True, null=True, verbose_name="包含")
    criteria = models.CharField(max_length=1024, blank=True, null=True, verbose_name="准则")
    exclude = models.CharField(max_length=1024, blank=True, null=True, verbose_name="排除")
    consider = models.CharField(max_length=1024, blank=True, null=True, verbose_name="考虑")
    icd10 = models.CharField(max_length=8, blank=True, null=True, verbose_name="ICD10")
    icpc2 = models.CharField(max_length=10, blank=True, null=True, verbose_name="ICPC2")
    note = models.CharField(max_length=1024, blank=True, null=True, verbose_name="备注")
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    def __str__(self):
        return str(self.iname)

    class Meta:
        abstract = True


# ICPC子类基类
class IcpcSubBase(IcpcBase):
    def save(self, *args, **kwargs):
        if self.iname:
            self.pym = ''.join(lazy_pinyin(self.iname, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# 自定义管理器增加备份功能
class BackupManager(models.Manager):
    def backup_data(self):
        backup_data = []
        for item in self.all():
            item_dict = model_to_dict(item)

            # 遍历模型字段，如果是外键，则用外键的hssc_id替换外键id
            for field in self.model._meta.fields:
                if item_dict[field.name]:  # 如果字段不为空，进行检查替换                    
                    if field.name in ['name_icpc', 'icpc']:  # 如果是ICPC外键，获取icpc_code
                        _object = field.related_model.objects.get(id=item_dict[field.name])
                        item_dict[field.name] = _object.icpc_code
                    else:
                        if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段, 获取外键的hssc_id
                            _object = field.related_model.objects.get(id=item_dict[field.name])
                            item_dict[field.name] = _object.hssc_id
                        elif field.many_to_many:  # 如果是多对多字段，获取外键的hssc_id
                            ids = []
                            for _object in field.related_model.objects.filter(id__in=item_dict[field.name]):
                                ids.append(_object.hssc_id)
                            item_dict[field.name] = ids
                        elif field.__class__.__name__ == 'DurationField':  # duration字段
                            item_dict[field.name] = str(item_dict[field.name])


            backup_data.append(item_dict)
   
        return backup_data


# Hssc基类
class HsscBase(models.Model):
    label = models.CharField(max_length=255, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")
    objects = BackupManager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.hssc_id is None:
            self.hssc_id = uuid.uuid1()
        super().save(*args, **kwargs)


class HsscPymBase(HsscBase):
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.label:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
