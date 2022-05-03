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

            # 恢复ManagedEntity的base_form字段
            # 说明：这是一个特殊处理，因为在恢复ManagedEntity时，base_form字段指向的BuessinessForm是不存在的，
            def restore_managed_entity_base_form():
                for entity in design_data['managedentity']:
                    entity_obj = ManagedEntity.objects.get(hssc_id=entity['hssc_id'])
                    if entity['base_form']:  
                        base_form = BuessinessForm.objects.get(hssc_id=entity['base_form'])
                        entity_obj.base_form = base_form
                        entity_obj.save()
                    if entity['header_fields']:  # 如果有header_fields字段，则恢复header_fields字段
                        header_fields = []
                        for _field in entity['header_fields']:
                            field_obj = Component.objects.get(hssc_id=_field)
                            header_fields.append(field_obj)
                        entity_obj.header_fields.set(header_fields)


            # 读取备份数据文件
            backuped_json_file = 'define_backup/design_data_backup.json'
            with open(backuped_json_file, encoding="utf8") as f:
                design_data = json.loads(f.read())


            Component.objects.all().delete()
            RelateFieldModel.objects.all().delete()
            for model in Backup_models:
                print(model._meta.model_name)
                if model == Service:  # 导入Service前先恢复ManagedEntity的base_form字段
                    restore_managed_entity_base_form()
                result = model.objects.restore_data(design_data[model._meta.model_name])
                print(result)
            
            print('恢复设计数据完成！')
