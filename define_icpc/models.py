from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from pypinyin import Style, lazy_pinyin

from hsscbase_class import IcpcBase, IcpcSubBase

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


