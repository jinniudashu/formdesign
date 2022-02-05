from django.core.management import BaseCommand
import requests
import json


class Command(BaseCommand):
    help = '从设计系统导入设计数据，保存为本地JSON文件'

    def handle(self, *args, **kwargs):

        # 获取脚本源码，创建文件
        print('开始导入设计数据备份...')
        # res = requests.get('https://hssc-formdesign.herokuapp.com/define_operand/design_backup/')
        res = requests.get('http://127.0.0.1:8000/define_operand/design_backup/')
        res_json = res.json()[0]
        code =res_json['code']

        with open('design_data_backup.json', 'w', encoding='utf-8') as f:
            f.write(code)

        print('备份设计数据到design_data_backup.json完成！')