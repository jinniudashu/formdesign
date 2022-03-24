from django.db import models
from django.forms.models import model_to_dict
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from pypinyin import Style, lazy_pinyin


icpc_list=[
	{'name': 'Icpc1_register_logins', 'label': '注册登录（行政管理）'},  # 28
	{'name': 'Icpc2_reservation_investigations', 'label': '预约咨询调查（行政管理）'},  # 19
	{'name': 'Icpc3_symptoms_and_problems', 'label': '症状和问题'},  # 1233
	{'name': 'Icpc4_physical_examination_and_tests', 'label': '体格和其他检查'},  # 241
	{'name': 'Icpc5_evaluation_and_diagnoses', 'label': '评估和诊断'},  # 4488
	{'name': 'Icpc6_prescribe_medicines', 'label': '开药'},  # 4
	{'name': 'Icpc7_treatments', 'label': '治疗'},  # 11
	{'name': 'Icpc8_other_health_interventions', 'label': '其他健康干预'},  # 13
	{'name': 'Icpc9_referral_consultations', 'label': '转诊会诊'},  # 8
	{'name': 'Icpc10_test_results_and_statistics', 'label': '检查结果和统计'},  # 5
]


# 自定义管理器增加ICPC备份和恢复功能
class IcpcBackupManager(models.Manager):
    def backup_data(self):
        icpc_data = []
        for item in self.all():
            item_dict = model_to_dict(item)
            item_dict.pop('id')  # 删除id字段
            icpc_data.append(item_dict)
        return icpc_data

    def restore_data(self, data):
        if data is None or len(data) == 0:
            return 'No data to restore'
        print('开始恢复：', self.model.__name__)
        self.all().delete()
        for item in data:
            self.create(**item)
        return f'{self.model.__name__} 数据导入成功'


# ICPC抽象类
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

    objects = IcpcBackupManager()

    def __str__(self):
        return str(self.iname)

    class Meta:
        abstract = True


# ICPC子类抽象类
class IcpcSubBase(IcpcBase):

    def save(self, *args, **kwargs):
        if self.iname:
            self.pym = ''.join(lazy_pinyin(self.iname, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# ICPC总表
class Icpc(IcpcBase):
    subclass = models.CharField(max_length=255, blank=True, null=True, verbose_name="ICPC子类")

    class Meta:
        verbose_name = "ICPC总表"
        verbose_name_plural = "ICPC总表"


class Icpc1_register_logins(IcpcSubBase):
    class Meta:
        verbose_name = "注册登录（行政管理）"
        verbose_name_plural = "注册登录（行政管理）"


class Icpc2_reservation_investigations(IcpcSubBase):
    class Meta:
        verbose_name = "预约咨询调查（行政管理）"
        verbose_name_plural = "预约咨询调查（行政管理）"


class Icpc3_symptoms_and_problems(IcpcSubBase):
    class Meta:
        verbose_name = "症状和问题"
        verbose_name_plural = "症状和问题"


class Icpc4_physical_examination_and_tests(IcpcSubBase):
    class Meta:
        verbose_name = "体格和其他检查"
        verbose_name_plural = "体格和其他检查"


class Icpc5_evaluation_and_diagnoses(IcpcSubBase):
    class Meta:
        verbose_name = "评估和诊断"
        verbose_name_plural = "评估和诊断"


class Icpc6_prescribe_medicines(IcpcSubBase):
    class Meta:
        verbose_name = "开药"
        verbose_name_plural = "开药"


class Icpc7_treatments(IcpcSubBase):
    class Meta:
        verbose_name = "治疗"
        verbose_name_plural = "治疗"


class Icpc8_other_health_interventions(IcpcSubBase):
    class Meta:
        verbose_name = "其他健康干预"
        verbose_name_plural = "其他健康干预"


class Icpc9_referral_consultations(IcpcSubBase):
    class Meta:
        verbose_name = "转诊会诊"
        verbose_name_plural = "转诊会诊"


class Icpc10_test_results_and_statistics(IcpcBase):
    class Meta:
        verbose_name = "检查结果和统计"
        verbose_name_plural = "检查结果和统计"


# 如果ICPC子类表项目有变化，则更新ICPC总表
@receiver(post_save, sender=Icpc1_register_logins, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc2_reservation_investigations, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc3_symptoms_and_problems, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc4_physical_examination_and_tests, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc5_evaluation_and_diagnoses, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc6_prescribe_medicines, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc7_treatments, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc8_other_health_interventions, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc9_referral_consultations, weak=True, dispatch_uid=None)
@receiver(post_save, sender=Icpc10_test_results_and_statistics, weak=True, dispatch_uid=None)
def icpc_post_save_handler(sender, instance, created, **kwargs):
	if created:
		Icpc.objects.create(
			icpc_code=instance.icpc_code,
			icode=instance.icode,
			iname=instance.iname,
			iename=instance.iename,
			include=instance.include,
			criteria=instance.criteria,
			exclude=instance.exclude,
			consider=instance.consider,
			icd10=instance.icd10,
			icpc2=instance.icpc2,
			note=instance.note,
			pym=instance.pym,
			subclass=instance._meta.object_name
		)
	else:
		Icpc.objects.filter(icpc_code=instance.icpc_code).update(
			icode=instance.icode,
			iname=instance.iname,
			iename=instance.iename,
			include=instance.include,
			criteria=instance.criteria,
			exclude=instance.exclude,
			consider=instance.consider,
			icd10=instance.icd10,
			icpc2=instance.icpc2,
			note=instance.note,
			pym=instance.pym,
			subclass=instance._meta.object_name
		)

@receiver(post_delete, sender=Icpc1_register_logins, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc2_reservation_investigations, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc3_symptoms_and_problems, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc4_physical_examination_and_tests, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc5_evaluation_and_diagnoses, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc6_prescribe_medicines, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc7_treatments, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc8_other_health_interventions, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc9_referral_consultations, weak=True, dispatch_uid=None)
@receiver(post_delete, sender=Icpc10_test_results_and_statistics, weak=True, dispatch_uid=None)
def icpc_post_delete_handler(sender, instance, **kwargs):
	Icpc.objects.filter(icpc_code=instance.icpc_code).delete()


