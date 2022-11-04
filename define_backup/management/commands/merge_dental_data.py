from django.core.management import BaseCommand
import json

from define.models import *
from define_operand.models import *


class Command(BaseCommand):
    help = 'Restore design data from backuped json file'

    def handle(self, *args, **options):
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

        # 表结构变更Model
        # Service: service_type
        # EventExpression: char_value, number_value

        for model in merge_models:
            print(model._meta.model_name)

            result = model.objects.merge_data(design_data[model._meta.model_name])

            print(result)
        
        print('恢复设计数据完成！')
