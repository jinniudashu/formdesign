from django.db import models


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


class Icpc1_register_logins(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "注册登录（行政管理）"
		verbose_name_plural = "注册登录（行政管理）"


class Icpc2_reservation_investigations(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "预约咨询调查（行政管理）"
		verbose_name_plural = "预约咨询调查（行政管理）"


class Icpc3_symptoms_and_problems(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname or ""

	class Meta:
		verbose_name = "症状和问题"
		verbose_name_plural = "症状和问题"


class Icpc4_physical_examination_and_tests(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "体格和其他检查"
		verbose_name_plural = "体格和其他检查"


class Icpc5_evaluation_and_diagnoses(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname or ""

	class Meta:
		verbose_name = "评估和诊断"
		verbose_name_plural = "评估和诊断"


class Icpc6_prescribe_medicines(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "开药"
		verbose_name_plural = "开药"


class Icpc7_treatments(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "治疗"
		verbose_name_plural = "治疗"


class Icpc8_other_health_interventions(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "其他健康干预"
		verbose_name_plural = "其他健康干预"


class Icpc9_referral_consultations(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "转诊会诊"
		verbose_name_plural = "转诊会诊"


class Icpc10_test_results_and_statistics(models.Model):
	icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")
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
		return self.iname

	class Meta:
		verbose_name = "检查结果和统计"
		verbose_name_plural = "检查结果和统计"


# 设计数据备份
class IcpcBackup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="版本")
    label = models.CharField(max_length=255, verbose_name="版本名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    code = models.TextField(verbose_name="源代码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ICPC数据备份"
        verbose_name_plural = "ICPC数据备份"
        ordering = ['id']
