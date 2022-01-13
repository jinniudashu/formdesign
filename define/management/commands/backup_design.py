import requests
import json
import time
from django.core.management import BaseCommand

# 写入文件
def write_to_file(file_name, content, mode='w'):
    # output_path = '.\\define\\'   # views.py urls.py 导出路径
    with open(f'{file_name}', mode, encoding='utf-8') as f:
        f.write(content)
    return      


class Command(BaseCommand):
    help = 'Backup design from https://hssc-formdesign.herokuapp.com/define and write to json file'

    def handle(self, *args, **options):
        # ***Create forms***
        url = 'https://hssc-rcms.herokuapp.com/forms'
        res = requests.get(url)
        res_json = res.json()
        print(res.status_code)
        write_to_file('rms_forms.json', json.dumps(res_json, indent=4, ensure_ascii=False))
