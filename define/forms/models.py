from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from time import time
from datetime import date
from django.utils import timezone

from icpc.models import *
from dictionaries.enums import *
from core.models import Staff, Customer

class Allergies_history(models.Model):
    relatedfield_drug_name = models.ForeignKey(Drug_list, on_delete=models.CASCADE, verbose_name='药品名称')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '过敏史'
        verbose_name_plural = '过敏史'

    def get_absolute_url(self):
        return reverse('allergies_history_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('allergies_history_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('allergies_history_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Out_of_hospital_self_report_survey(models.Model):
    relatedfield_symptom_list = models.ForeignKey(Icpc3_symptoms_and_problems, on_delete=models.CASCADE, verbose_name='症状')
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '院外症状自述调查'
        verbose_name_plural = '院外症状自述调查'

    def get_absolute_url(self):
        return reverse('out_of_hospital_self_report_survey_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('out_of_hospital_self_report_survey_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('out_of_hospital_self_report_survey_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_comprehensive_psychological_quality_survey(models.Model):
    relatedfield_personality_tendency = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='性格倾向')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人心理综合素质调查'
        verbose_name_plural = '个人心理综合素质调查'

    def get_absolute_url(self):
        return reverse('personal_comprehensive_psychological_quality_survey_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_comprehensive_psychological_quality_survey_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_comprehensive_psychological_quality_survey_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_adaptability_assessment(models.Model):
    characterfield_working_hours_per_day = models.TextField(max_length=255, null=True, blank=True, verbose_name='每天工作及工作往返总时长')
    relatedfield_are_you_satisfied_with_the_job_and_life = models.ForeignKey(Satisfaction, on_delete=models.CASCADE, verbose_name='对目前生活和工作满意吗')
    relatedfield_are_you_satisfied_with_your_adaptability = models.ForeignKey(Satisfaction, on_delete=models.CASCADE, verbose_name='对自己的适应能力满意吗')
    relatedfield_can_you_get_encouragement_and_support_from_family_and_friends = models.ForeignKey(Frequency, on_delete=models.CASCADE, verbose_name='是否能得到家人朋友的鼓励和支持')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人适应能力评估'
        verbose_name_plural = '个人适应能力评估'

    def get_absolute_url(self):
        return reverse('personal_adaptability_assessment_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_adaptability_assessment_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_adaptability_assessment_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_health_behavior_survey(models.Model):
    relatedfield_drinking_frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE, verbose_name='饮酒频次')
    relatedfield_smoking_frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE, verbose_name='吸烟频次')
    characterfield_average_sleep_duration = models.CharField(max_length=255, null=True, blank=True, verbose_name='平均睡眠时长')
    characterfield_duration_of_insomnia = models.CharField(max_length=255, null=True, blank=True, verbose_name='持续失眠时间')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人健康行为调查'
        verbose_name_plural = '个人健康行为调查'

    def get_absolute_url(self):
        return reverse('personal_health_behavior_survey_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_health_behavior_survey_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_health_behavior_survey_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_health_assessment(models.Model):
    relatedfield_own_health = models.ForeignKey(State_degree, on_delete=models.CASCADE, verbose_name='觉得自身健康状况如何')
    relatedfield_compared_to_last_year = models.ForeignKey(Comparative_expression, on_delete=models.CASCADE, verbose_name='较之过去一年状态如何')
    relatedfield_sports_preference = models.ForeignKey(Sports_preference, on_delete=models.CASCADE, verbose_name='运动偏好')
    relatedfield_exercise_time = models.ForeignKey(Exercise_time, on_delete=models.CASCADE, verbose_name='运动时长')
    relatedfield_have_any_recent_symptoms_of_physical_discomfort = models.ForeignKey(Icpc3_symptoms_and_problems, on_delete=models.CASCADE, verbose_name='近来有无身体不适症状')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人身体健康评估'
        verbose_name_plural = '个人身体健康评估'

    def get_absolute_url(self):
        return reverse('personal_health_assessment_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_health_assessment_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_health_assessment_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Social_environment_assessment(models.Model):
    relatedfield_is_the_living_environment_satisfactory = models.ForeignKey(Satisfaction, on_delete=models.CASCADE, verbose_name='您对居住环境满意吗')
    relatedfield_is_the_transportation_convenient = models.ForeignKey(Convenience, on_delete=models.CASCADE, verbose_name='您所在的社区交通方便吗')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '社会环境评估'
        verbose_name_plural = '社会环境评估'

    def get_absolute_url(self):
        return reverse('social_environment_assessment_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('social_environment_assessment_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('social_environment_assessment_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Vital_signs_check(models.Model):
    numberfield_body_temperature = models.IntegerField(null=True, blank=True, verbose_name='体温')
    numberfield_body_temperature_standard_value = models.IntegerField(null=True, blank=True, verbose_name='体温标准值')
    numberfield_body_temperature_up_limit = models.IntegerField(default=37.4, null=True, blank=True, verbose_name='体温上限')
    numberfield_body_temperature_down_limit = models.IntegerField(default=36.0, null=True, blank=True, verbose_name='体温下限')
    numberfield_pulse = models.IntegerField(null=True, blank=True, verbose_name='脉搏')
    numberfield_pulse_standard_value = models.IntegerField(null=True, blank=True, verbose_name='脉搏标准值')
    numberfield_pulse_up_limit = models.IntegerField(default=100.0, null=True, blank=True, verbose_name='脉搏上限')
    numberfield_pulse_down_limit = models.IntegerField(default=60.0, null=True, blank=True, verbose_name='脉搏下限')
    numberfield_respiratory_rate = models.IntegerField(null=True, blank=True, verbose_name='呼吸频率')
    numberfield_respiratory_rate_standard_value = models.IntegerField(null=True, blank=True, verbose_name='呼吸频率标准值')
    numberfield_respiratory_rate_up_limit = models.IntegerField(default=20.0, null=True, blank=True, verbose_name='呼吸频率上限')
    numberfield_respiratory_rate_down_limit = models.IntegerField(default=10.0, null=True, blank=True, verbose_name='呼吸频率下限')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '生命体征检查'
        verbose_name_plural = '生命体征检查'

    def get_absolute_url(self):
        return reverse('vital_signs_check_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('vital_signs_check_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('vital_signs_check_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Family_history_of_illness(models.Model):
    relatedfield_diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, on_delete=models.CASCADE, verbose_name='病名')
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, on_delete=models.CASCADE, verbose_name='家庭成员关系')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '家族病史'
        verbose_name_plural = '家族病史'

    def get_absolute_url(self):
        return reverse('family_history_of_illness_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('family_history_of_illness_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('family_history_of_illness_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination(models.Model):
    numberfield_hight = models.IntegerField(null=True, blank=True, verbose_name='身高')
    numberfield_hight_standard_value = models.IntegerField(null=True, blank=True, verbose_name='身高标准值')
    numberfield_hight_up_limit = models.IntegerField(null=True, blank=True, verbose_name='身高上限')
    numberfield_hight_down_limit = models.IntegerField(null=True, blank=True, verbose_name='身高下限')
    numberfield_weight = models.IntegerField(null=True, blank=True, verbose_name='体重')
    numberfield_weight_standard_value = models.IntegerField(null=True, blank=True, verbose_name='体重标准值')
    numberfield_weight_up_limit = models.IntegerField(null=True, blank=True, verbose_name='体重上限')
    numberfield_weight_down_limit = models.IntegerField(null=True, blank=True, verbose_name='体重下限')
    numberfield_body_mass_index = models.IntegerField(null=True, blank=True, verbose_name='体质指数')
    numberfield_body_mass_index_standard_value = models.IntegerField(null=True, blank=True, verbose_name='体质指数标准值')
    numberfield_body_mass_index_up_limit = models.IntegerField(default=23.9, null=True, blank=True, verbose_name='体质指数上限')
    numberfield_body_mass_index_down_limit = models.IntegerField(default=18.5, null=True, blank=True, verbose_name='体质指数下限')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '体格检查'
        verbose_name_plural = '体格检查'

    def get_absolute_url(self):
        return reverse('physical_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_blood_transfusion(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    numberfield_blood_transfusion = models.IntegerField(null=True, blank=True, verbose_name='输血量')
    numberfield_blood_transfusion_standard_value = models.IntegerField(null=True, blank=True, verbose_name='输血量标准值')
    numberfield_blood_transfusion_up_limit = models.IntegerField(default=400.0, null=True, blank=True, verbose_name='输血量上限')
    numberfield_blood_transfusion_down_limit = models.IntegerField(null=True, blank=True, verbose_name='输血量下限')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '输血史'
        verbose_name_plural = '输血史'

    def get_absolute_url(self):
        return reverse('history_of_blood_transfusion_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_blood_transfusion_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_blood_transfusion_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_trauma(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    relatedfield_diseases_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, on_delete=models.CASCADE, verbose_name='病名')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '外伤史'
        verbose_name_plural = '外伤史'

    def get_absolute_url(self):
        return reverse('history_of_trauma_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_trauma_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_trauma_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Fundus_examination(models.Model):
    relatedfield_fundus = models.ForeignKey(Normality, on_delete=models.CASCADE, verbose_name='眼底')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '眼底检查'
        verbose_name_plural = '眼底检查'

    def get_absolute_url(self):
        return reverse('fundus_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('fundus_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('fundus_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Medical_history(models.Model):
    relatedfield_disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, on_delete=models.CASCADE, verbose_name='疾病名称')
    datetimefield_time_of_diagnosis = models.DateTimeField(null=True, blank=True, verbose_name='确诊时间')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '疾病史'
        verbose_name_plural = '疾病史'

    def get_absolute_url(self):
        return reverse('medical_history_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('medical_history_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('medical_history_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Doctor_registry(models.Model):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_contact_information = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    relatedfield_service_role = models.ForeignKey(Service_role, on_delete=models.CASCADE, verbose_name='服务角色')
    characterfield_practice_qualification = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    characterfield_password_setting = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码设置')
    characterfield_confirm_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='确认密码')
    characterfield_expertise = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    characterfield_practice_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    relatedfield_affiliation = models.ForeignKey(Institutions_list, on_delete=models.CASCADE, verbose_name='所属机构')
    datetimefield_date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name='出生日期')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '医生注册'
        verbose_name_plural = '医生注册'

    def get_absolute_url(self):
        return reverse('doctor_registry_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('doctor_registry_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('doctor_registry_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class User_login(models.Model):
    characterfield_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户名')
    characterfield_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '用户登录'
        verbose_name_plural = '用户登录'

    def get_absolute_url(self):
        return reverse('user_login_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('user_login_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('user_login_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Doctor_login(models.Model):
    characterfield_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户名')
    characterfield_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码')
    characterfield_service_role = models.CharField(max_length=255, null=True, blank=True, verbose_name='服务角色')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '医生登陆'
        verbose_name_plural = '医生登陆'

    def get_absolute_url(self):
        return reverse('doctor_login_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('doctor_login_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('doctor_login_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Dorsal_artery_pulsation_examination(models.Model):
    relatedfield_left_foot = models.ForeignKey(Dorsal_artery_pulsation, on_delete=models.CASCADE, verbose_name='左脚')
    relatedfield_right_foot = models.ForeignKey(Dorsal_artery_pulsation, on_delete=models.CASCADE, verbose_name='右脚')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '足背动脉搏动检查'
        verbose_name_plural = '足背动脉搏动检查'

    def get_absolute_url(self):
        return reverse('dorsal_artery_pulsation_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('dorsal_artery_pulsation_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('dorsal_artery_pulsation_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_hearing(models.Model):
    relatedfield_left_ear_hearing = models.ForeignKey(Hearing, on_delete=models.CASCADE, verbose_name='左耳听力')
    relatedfield_right_ear_hearing = models.ForeignKey(Hearing, on_delete=models.CASCADE, verbose_name='右耳听力')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体听力'
        verbose_name_plural = '查体听力'

    def get_absolute_url(self):
        return reverse('physical_examination_hearing_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_hearing_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_hearing_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_infectious_diseases(models.Model):
    relatedfield_diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, on_delete=models.CASCADE, verbose_name='病名')
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, on_delete=models.CASCADE, verbose_name='家庭成员关系')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '遗传病史'
        verbose_name_plural = '遗传病史'

    def get_absolute_url(self):
        return reverse('history_of_infectious_diseases_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_infectious_diseases_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_infectious_diseases_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_surgery(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    relatedfield_name_of_operation = models.ForeignKey(Icpc7_treatments, on_delete=models.CASCADE, verbose_name='手术名称')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '手术史'
        verbose_name_plural = '手术史'

    def get_absolute_url(self):
        return reverse('history_of_surgery_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_surgery_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_surgery_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_oral_cavity(models.Model):
    relatedfield_lips = models.ForeignKey(Lips, on_delete=models.CASCADE, verbose_name='口唇')
    relatedfield_dentition = models.ForeignKey(Dentition, on_delete=models.CASCADE, verbose_name='齿列')
    relatedfield_pharynx = models.ForeignKey(Pharynx, on_delete=models.CASCADE, verbose_name='咽部')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体口腔'
        verbose_name_plural = '查体口腔'

    def get_absolute_url(self):
        return reverse('physical_examination_oral_cavity_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_oral_cavity_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_oral_cavity_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Blood_pressure_monitoring(models.Model):
    numberfield_systolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    numberfield_systolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='收缩压标准值')
    numberfield_systolic_blood_pressure_up_limit = models.IntegerField(default=139.0, null=True, blank=True, verbose_name='收缩压上限')
    numberfield_systolic_blood_pressure_down_limit = models.IntegerField(default=90.0, null=True, blank=True, verbose_name='收缩压下限')
    numberfield_diastolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    numberfield_diastolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='舒张压标准值')
    numberfield_diastolic_blood_pressure_up_limit = models.IntegerField(default=89.0, null=True, blank=True, verbose_name='舒张压上限')
    numberfield_diastolic_blood_pressure_down_limit = models.IntegerField(default=60.0, null=True, blank=True, verbose_name='舒张压下限')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '血压监测'
        verbose_name_plural = '血压监测'

    def get_absolute_url(self):
        return reverse('blood_pressure_monitoring_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('blood_pressure_monitoring_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('blood_pressure_monitoring_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Major_life_events(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    relatedfield_major_life = models.ForeignKey(Life_event, on_delete=models.CASCADE, verbose_name='生活事件')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '重大生活事件调查'
        verbose_name_plural = '重大生活事件调查'

    def get_absolute_url(self):
        return reverse('major_life_events_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('major_life_events_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('major_life_events_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_vision(models.Model):
    characterfield_left_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='左眼视力')
    characterfield_right_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='右眼视力')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体视力'
        verbose_name_plural = '查体视力'

    def get_absolute_url(self):
        return reverse('physical_examination_vision_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_vision_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_vision_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Lower_extremity_edema_examination(models.Model):
    relatedfield_lower_extremity_edema = models.ForeignKey(Edema, on_delete=models.CASCADE, verbose_name='下肢水肿')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '下肢水肿检查'
        verbose_name_plural = '下肢水肿检查'

    def get_absolute_url(self):
        return reverse('lower_extremity_edema_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('lower_extremity_edema_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('lower_extremity_edema_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Basic_personal_information(models.Model):
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, on_delete=models.CASCADE, verbose_name='家庭成员关系')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    datetimefield_date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name='出生日期')
    relatedfield_family_id = models.ForeignKey(Icpc1_register_logins, on_delete=models.CASCADE, verbose_name='家庭编号')
    characterfield_resident_file_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='居民档案号')
    relatedfield_gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name='性别')
    relatedfield_nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, verbose_name='民族')
    relatedfield_marital_status = models.ForeignKey(Marital_status, on_delete=models.CASCADE, verbose_name='婚姻状况')
    relatedfield_education = models.ForeignKey(Education, on_delete=models.CASCADE, verbose_name='文化程度')
    relatedfield_occupational_status = models.ForeignKey(Occupational_status, on_delete=models.CASCADE, verbose_name='职业状况')
    characterfield_family_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_medical_ic_card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='医疗ic卡号')
    relatedfield_medical_expenses_burden = models.ForeignKey(Medical_expenses_burden, on_delete=models.CASCADE, verbose_name='医疗费用负担')
    relatedfield_type_of_residence = models.ForeignKey(Type_of_residence, on_delete=models.CASCADE, verbose_name='居住类型')
    relatedfield_blood_type = models.ForeignKey(Blood_type, on_delete=models.CASCADE, verbose_name='血型')
    relatedfield_signed_family_doctor = models.ForeignKey(Employee_list, on_delete=models.CASCADE, verbose_name='签约家庭医生')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人基本情况'
        verbose_name_plural = '个人基本情况'

    def get_absolute_url(self):
        return reverse('basic_personal_information_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('basic_personal_information_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('basic_personal_information_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_athletic_ability(models.Model):
    relatedfield_athletic_ability = models.ForeignKey(Exercise_time, on_delete=models.CASCADE, verbose_name='运动能力')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体运动能力'
        verbose_name_plural = '查体运动能力'

    def get_absolute_url(self):
        return reverse('physical_examination_athletic_ability_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_athletic_ability_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_athletic_ability_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class User_registry(models.Model):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_contact_information = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_password_setting = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码设置')
    characterfield_confirm_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='确认密码')
    datetimefield_date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name='出生日期')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '用户注册表'
        verbose_name_plural = '用户注册表'

    def get_absolute_url(self):
        return reverse('user_registry_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('user_registry_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('user_registry_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

