from django.core.management import BaseCommand
import json

from define.models import *
from define_operand.models import *
from define_icpc.models import Icpc
from define_backup.backup_data import Backup_models


class Command(BaseCommand):
    help = 'Restore design data from backuped json file'

    def handle(self, *args, **options):

        # 如果是在生产系统上运行，请确认设计数据backup_design是最新版本的备份
        make_sure = input('''如果当前是在生产系统上操作，请确认设计数据backup_design是最新版本的备份！\n是否要开始恢复设计数据操作？(y/n)''')
        if make_sure != 'y':
            print('Cancel restore design data...')
            return
        else:
            print('start restore design data...')

            # 读取备份数据文件
            backuped_json_file = 'define_backup/design_data_backup.json'
            with open(backuped_json_file, encoding="utf8") as f:
                design_data = json.loads(f.read())

            Component.objects.all().delete()
            RelateFieldModel.objects.all().delete()
            for model in Backup_models:
                print(model._meta.model_name)
                result = model.objects.restore_data(design_data[model._meta.model_name])
                print(result)
                
            print('恢复设计数据完成！')
