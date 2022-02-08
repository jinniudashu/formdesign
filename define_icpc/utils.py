########################################################################################################################
# ICPC数据备份
########################################################################################################################
from django.forms.models import model_to_dict
from time import time
import json
from define_icpc.models import icpc_list, IcpcBackup, Icpc1_register_logins, Icpc2_reservation_investigations, Icpc3_symptoms_and_problems, Icpc4_physical_examination_and_tests, Icpc5_evaluation_and_diagnoses, Icpc6_prescribe_medicines, Icpc7_treatments, Icpc8_other_health_interventions, Icpc9_referral_consultations, Icpc10_test_results_and_statistics

def icpc_backup(modeladmin, request, queryset):
    icpc_data = {}
    for icpc in icpc_list:
        _key = icpc['name'].lower()
        icpc_data[_key] = []
        Icpc_model = eval(icpc['name'])
        for item in Icpc_model.objects.all():            
            icpc_data[_key].append(model_to_dict(item))
    # print(icpc_data)

    # 写入数据库
    s = IcpcBackup.objects.create(
        name = str(int(time())),
        code = json.dumps(icpc_data, indent=4, ensure_ascii=False),
    )
    print(f'设计数据备份成功, id: {s.id}')

icpc_backup.short_description = '备份ICPC数据'
