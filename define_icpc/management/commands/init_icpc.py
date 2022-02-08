from django.core.management import BaseCommand
import requests
import json, math
from define_icpc.models import icpc_list, Icpc1_register_logins, Icpc2_reservation_investigations, Icpc3_symptoms_and_problems, Icpc4_physical_examination_and_tests, Icpc5_evaluation_and_diagnoses, Icpc6_prescribe_medicines, Icpc7_treatments, Icpc8_other_health_interventions, Icpc9_referral_consultations, Icpc10_test_results_and_statistics

class Command(BaseCommand):
    help = '初始化导入ICPC数据'

    def handle(self, *args, **kwargs):
        params = '?_publicationState=preview'

        for icpc in icpc_list:
            url = f'https://hssc-rcms.herokuapp.com/{icpc["url"]}'
            print(f'从{url}导入ICPC数据...')
            print('正在查询总记录数……')
            res = requests.get(f'{url}/count?_publicationState=preview')
            print(f'{res.text}条记录正在导入：{url}')

            pages_counter = math.ceil(int(res.text)/100)
            page = 1
            i = 0

            Icpc_model= eval(icpc['name'])  # 把model名称转为 model class
            Icpc_model.objects.all().delete()  # 删除原有数据
            
            # 每100条记录GET一次
            while page <= pages_counter:
                res = requests.get(f'{url}?_publicationState=preview&_start={(page-1)*100}')
                res_json = res.json()
                for obj in res_json:
                    i += 1
                    try:
                        Icpc_model.objects.create(
                            icpc_code = obj['icpc_code'],
                            icode = obj['icode'],
                            iname = obj['iname'],
                            iename = obj['iename'],
                            include = obj['include'],
                            criteria = obj['criteria'],
                            exclude = obj['exclude'],
                            consider = obj['consider'],
                            icd10 = obj['icd10'],
                            icpc2 = obj['icpc2'],
                            note = obj['note'],
                            pym = obj['pym'],
                        )
                    except Exception as e:
                        print (f'{e}:{i}')
                    else:
                        print (f'{i}')
                page += 1
            print(f'成功导入{i}条记录')

        print('导入ICPC数据完成')