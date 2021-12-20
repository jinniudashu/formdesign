from django.contrib import admin
from .models import *
    
class Allergies_historyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(Allergies_history, Allergies_historyAdmin)

class Out_of_hospital_self_report_surveyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(Out_of_hospital_self_report_survey, Out_of_hospital_self_report_surveyAdmin)

class Personal_comprehensive_psychological_quality_surveyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_personality_tendency", ]
admin.site.register(Personal_comprehensive_psychological_quality_survey, Personal_comprehensive_psychological_quality_surveyAdmin)

class Personal_adaptability_assessmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_are_you_satisfied_with_the_job_and_life", "relatedfield_are_you_satisfied_with_your_adaptability", "relatedfield_can_you_get_encouragement_and_support_from_family_and_friends", ]
admin.site.register(Personal_adaptability_assessment, Personal_adaptability_assessmentAdmin)

class Personal_health_behavior_surveyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drinking_frequency", "relatedfield_smoking_frequency", ]
admin.site.register(Personal_health_behavior_survey, Personal_health_behavior_surveyAdmin)

class Personal_health_assessmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_own_health", "relatedfield_compared_to_last_year", "relatedfield_sports_preference", "relatedfield_exercise_time", "relatedfield_have_any_recent_symptoms_of_physical_discomfort", ]
admin.site.register(Personal_health_assessment, Personal_health_assessmentAdmin)

class Social_environment_assessmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_is_the_living_environment_satisfactory", "relatedfield_is_the_transportation_convenient", ]
admin.site.register(Social_environment_assessment, Social_environment_assessmentAdmin)

admin.site.register(Vital_signs_check)

class Family_history_of_illnessAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_diseases", "relatedfield_family_relationship", ]
admin.site.register(Family_history_of_illness, Family_history_of_illnessAdmin)

admin.site.register(Physical_examination)

admin.site.register(History_of_blood_transfusion)

class History_of_traumaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_diseases_name", ]
admin.site.register(History_of_trauma, History_of_traumaAdmin)

class Fundus_examinationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_fundus", ]
admin.site.register(Fundus_examination, Fundus_examinationAdmin)

class Medical_historyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_disease_name", ]
admin.site.register(Medical_history, Medical_historyAdmin)

class Doctor_registryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_service_role", "relatedfield_affiliation", ]
admin.site.register(Doctor_registry, Doctor_registryAdmin)

admin.site.register(User_login)

admin.site.register(Doctor_login)

class Dorsal_artery_pulsation_examinationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_left_foot", "relatedfield_right_foot", ]
admin.site.register(Dorsal_artery_pulsation_examination, Dorsal_artery_pulsation_examinationAdmin)

class Physical_examination_hearingAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", ]
admin.site.register(Physical_examination_hearing, Physical_examination_hearingAdmin)

class History_of_infectious_diseasesAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_diseases", "relatedfield_family_relationship", ]
admin.site.register(History_of_infectious_diseases, History_of_infectious_diseasesAdmin)

class History_of_surgeryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_name_of_operation", ]
admin.site.register(History_of_surgery, History_of_surgeryAdmin)

class Physical_examination_oral_cavityAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", ]
admin.site.register(Physical_examination_oral_cavity, Physical_examination_oral_cavityAdmin)

admin.site.register(Blood_pressure_monitoring)

class Major_life_eventsAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_major_life", ]
admin.site.register(Major_life_events, Major_life_eventsAdmin)

admin.site.register(Physical_examination_vision)

class Lower_extremity_edema_examinationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_lower_extremity_edema", ]
admin.site.register(Lower_extremity_edema_examination, Lower_extremity_edema_examinationAdmin)

class Basic_personal_informationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_family_relationship", "relatedfield_family_id", "relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", ]
admin.site.register(Basic_personal_information, Basic_personal_informationAdmin)

class Physical_examination_athletic_abilityAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_athletic_ability", ]
admin.site.register(Physical_examination_athletic_ability, Physical_examination_athletic_abilityAdmin)

admin.site.register(User_registry)
