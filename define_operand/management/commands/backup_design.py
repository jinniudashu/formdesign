from django.core.management import BaseCommand
import requests
import json


class Command(BaseCommand):
    help = '从设计系统导入设计数据，保存为本地JSON文件'

    def handle(self, *args, **kwargs):
        url = 'https://hssc-formdesign.herokuapp.com/define_operand/design_backup/'
        # url = 'http://127.0.0.1:8000/define_operand/design_backup/'
        print(f'从{url}导入设计数据备份...')
        res = requests.get(url)
        res_json = res.json()[0]
        code =res_json['code']

        with open('design_data_backup.json', 'w', encoding='utf-8') as f:
            f.write(code)

        print('备份设计数据到design_data_backup.json完成！')