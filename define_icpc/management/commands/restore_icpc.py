from django.core.management import BaseCommand
import json

from define_icpc.models import icpc_list, IcpcBackup, Icpc1_register_logins, Icpc2_reservation_investigations, Icpc3_symptoms_and_problems, Icpc4_physical_examination_and_tests, Icpc5_evaluation_and_diagnoses, Icpc6_prescribe_medicines, Icpc7_treatments, Icpc8_other_health_interventions, Icpc9_referral_consultations, Icpc10_test_results_and_statistics

class Command(BaseCommand):
    help = 'Import ICPC data from json file'

    def handle(self, *args, **options):
        # 读取ICPC备份数据文件
        with open('icpc_backup.json', encoding="utf8") as f:
            icpc_data = json.loads(f.read())

        for icpc in icpc_list:
            Icpc_model = eval(icpc['name'])  # 反射出model
            _key = icpc['name'].lower()  # 获取小写键名
            _l = len(icpc_data[_key])  # 当前ICPC数据的长度

            Icpc_model.objects.all().delete()  # 删除ICPC数据
            print(f'正在导入{icpc["name"]}，共{_l}条记录...')
            for item in icpc_data[_key]:  # 导入ICPC数据
                Icpc_model.objects.create(**item)
            print(f'{icpc["name"]} 数据导入成功')
