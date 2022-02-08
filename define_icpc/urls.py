from django.urls import path
from .views import get_icpc_backup, get_icpc1_register_logins, get_icpc2_reservation_investigations, get_icpc3_symptoms_and_problems, get_icpc4_physical_examination_and_tests, get_icpc5_evaluation_and_diagnoses, get_icpc6_prescribe_medicines, get_icpc7_treatments, get_icpc8_other_health_interventions, get_icpc9_referral_consultations, get_icpc10_test_results_and_statistics

urlpatterns = [
    path('get_icpc1_register_logins/', get_icpc1_register_logins, name='get_icpc1_register_logins'),
    path('get_icpc2_reservation_investigations/', get_icpc2_reservation_investigations, name='get_icpc2_reservation_investigations'),
    path('get_icpc3_symptoms_and_problems/', get_icpc3_symptoms_and_problems, name='get_icpc3_symptoms_and_problems'),
    path('get_icpc4_physical_examination_and_tests/', get_icpc4_physical_examination_and_tests, name='get_icpc4_physical_examination_and_tests'),
    path('get_icpc5_evaluation_and_diagnoses/', get_icpc5_evaluation_and_diagnoses, name='get_icpc5_evaluation_and_diagnoses'),
    path('get_icpc6_prescribe_medicines/', get_icpc6_prescribe_medicines, name='get_icpc6_prescribe_medicines'),
    path('get_icpc7_treatments/', get_icpc7_treatments, name='get_icpc7_treatments'),
    path('get_icpc8_other_health_interventions/', get_icpc8_other_health_interventions, name='get_icpc8_other_health_interventions'),
    path('get_icpc9_referral_consultations/', get_icpc9_referral_consultations, name='get_icpc9_referral_consultations'),
    path('get_icpc10_test_results_and_statistics/', get_icpc10_test_results_and_statistics, name='get_icpc10_test_results_and_statistics'),
    path('get_icpc_backup/', get_icpc_backup, name='get_icpc_backup'),
]