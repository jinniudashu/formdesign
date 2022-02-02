from django.core.management import BaseCommand
import json

from define.models import BoolField, CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component
from define_form.models import ManagedEntity, BaseModel, BaseForm, CombineForm
from define_operand.models import OperandView
from define_dict.models import DicList

from design_data_backup import design_data

class Command(BaseCommand):
    help = 'Import design from json file'

    def handle(self, *args, **options):
        # 读取备份数据文件
        with open('design_data_backup.json', encoding="utf8") as f:
            design_data = json.loads(f.read())

        # 删除所有数据
        ManagedEntity.objects.all().delete()
        DicList.objects.all().delete()
        BoolField.objects.all().delete()
        CharacterField.objects.all().delete()
        NumberField.objects.all().delete()
        DTField.objects.all().delete()
        ChoiceField.objects.all().delete()
        RelatedField.objects.all().delete()
        Component.objects.all().delete()
        BaseModel.objects.all().delete()
        BaseForm.objects.all().delete()
        CombineForm.objects.all().delete()
        OperandView.objects.all().delete()

        # 依序导入数据
        for model in design_data:
        # 导入管理实体表
            if model == 'managedentities':
                for item in design_data[model]:
                    ManagedEntity.objects.create(
                        name=item['name'],
                        label=item['label'],
                        description=item['description'],
                    )
        # 导入字典表
            elif model == 'diclists':
                for item in design_data[model]:
                    DicList.objects.create(
                        name=item['name'],
                        label=item['label'],
                        related_field=item['related_field'],
                        content=item['content'],
                    )
        # 导入字段表
            elif model == 'boolfields':
                for item in design_data[model]:
                    BoolField.objects.create(
                        name=item['name'],
                        label=item['label'],
                        type=item['type'],
                        required=item['required'],
                        default=item['default'],
                    )
            elif model == 'characterfields':
                for item in design_data[model]:
                    CharacterField.objects.create(
                        name=item['name'],
                        label=item['label'],
                        type=item['type'],
                        length=item['length'],
                        required=item['required'],
                        default=item['default'],
                    )
            elif model == 'numberfields':
                for item in design_data[model]:
                    NumberField.objects.create(
                        name=item['name'],
                        label=item['label'],
                        type=item['type'],
                        max_digits=item['max_digits'],
                        decimal_places=item['decimal_places'],
                        standard_value=item['standard_value'],
                        up_limit=item['up_limit'],
                        down_limit=item['down_limit'],
                        unit=item['unit'],
                        default=item['default'],
                        required=item['required'],
                    )
            elif model == 'dtfields':
                for item in design_data[model]:
                    DTField.objects.create(
                        name=item['name'],
                        label=item['label'],
                        type=item['type'],
                        default_now=item['default_now'],
                        required=item['required'],
                    )
            elif model == 'choicefields':
                for item in design_data[model]:
                    ChoiceField.objects.create(
                        name=item['name'],
                        label=item['label'],
                        type=item['type'],
                        options=item['options'],
                        default_first=item['default_first'],
                        required=item['required'],
                    )
            elif model == 'relatedfields':
                for item in design_data[model]:
                    dic=DicList.objects.get(name=item['related_content'])
                    RelatedField.objects.create(
                        name=item['name'],
                        label=item['label'],
                        type=item['type'],
                        related_content=dic,
                        related_field=item['related_field'],
                    )
        # 导入模型表
            elif model == 'basemodels':
                for item in design_data[model]:
                    print(item)
                    basemodel = BaseModel.objects.create(
                        name=item['name'],
                        label=item['label'],
                        description=item['description'],
                        is_base_infomation=item['is_base_infomation'],
                    )

                    model_components = []
                    for _component in item['components']:
                        component = Component.objects.get(name=_component['name'])
                        model_components.append(component)
                    basemodel.components.set(model_components)

                    model_managedentities = []
                    for _managedentity in item['managed_entity']:
                        managedentity = ManagedEntity.objects.get(name=_managedentity['name'])
                        model_managedentities.append(managedentity)
                    basemodel.managed_entity.set(model_managedentities)

        # 导入表单表
            elif model == 'baseforms':
                for item in design_data[model]:
                    baseform = BaseForm.objects.create(
                        name=item['name'],
                        label=item['label'],
                        basemodel=BaseModel.objects.get(name=item['basemodel']),
                        is_inquiry=item['is_inquiry'],
                        style=item['style'],
                    )

                    form_components = []
                    for _component in item['components']:
                        component = Component.objects.get(name=_component['name'])
                        form_components.append(component)
                    baseform.components.set(form_components)

        # 导入组合表单表
            elif model == 'combineforms':
                for item in design_data[model]:
                    if item['managed_entity']:
                        managed_entity=ManagedEntity.objects.get(name=item['managed_entity'])
                    else:
                        managed_entity=None
                    print(item)
                    combineform = CombineForm.objects.create(
                        name=item['name'],
                        label=item['label'],
                        is_base=item['is_base'],
                        managed_entity=managed_entity,
                    )

                for item in design_data[model]:
                    combineform = CombineForm.objects.get(name=item['name'])                
                    forms = []
                    for _form in item['forms']:
                        print(_form)
                        form = CombineForm.objects.get(name=_form)
                        forms.append(form)
                    combineform.forms.set(forms)

        # 导入操作表
            elif model == 'operandviews':
                for item in design_data[model]:
                    if item['managed_entity']:
                        managed_entity=ManagedEntity.objects.get(name=item['managed_entity'])
                    else:
                        managed_entity=None
                    print('OperandView:', item)
                    OperandView.objects.create(
                        name=item['name'],
                        label=item['label'],
                        managed_entity=managed_entity,
                        forms=CombineForm.objects.get(name=item['forms']),    
                    )

