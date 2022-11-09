from django.core.management import BaseCommand
import json

from define.models import *
from define_operand.models import *


class Command(BaseCommand):
    help = 'Restore design data from backuped json file'

    def handle(self, *args, **options):
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

        # 读取合并数据文件
        merge_json_file = 'define_backup/dental_design_data_backup.json'
        with open(merge_json_file, encoding="utf8") as f:
            design_data = json.loads(f.read())

        merge_models = [
            SystemOperand,
            CycleUnit,
            Role, 
            IcpcList,
            DicList, 
            DicDetail,
            ManagedEntity, 
            CharacterField,
            NumberField,
            DTField,
            RelatedField,
            FileField,
            ComponentsGroup,
            BuessinessForm,
            FormComponentsSetting,
            Service,
            BuessinessFormsSetting,
            EventRule,
            EventExpression,
            ServicePackage,
            ServicePackageDetail,
            ServiceRule,
            ExternalServiceMapping,
            ExternalServiceFieldsMapping,
        ]

        # Model字段变更处理
        # ManagedEntity：1.重新生成hssc_id; 2.手工补全project.hssc_id: b97e01a1-576d-11ed-a1bc-4889e7cf38c9
        # Project: Update Dental['roles','services','service_packages','service_rules','external_services']

        for model in merge_models:
            print(model._meta.model_name)

            if model == Service:  # 导入Service前先恢复ManagedEntity的base_form字段
                restore_managed_entity_base_form()

            result = model.objects.merge_data(design_data[model._meta.model_name])

            print(result)
        
        print('合并设计数据完成！')
