from django.core.management import BaseCommand
import json
from django.db.models.fields import related

from pypinyin import lazy_pinyin

from define.models import BoolField, CharacterField, DicList, NumberField, DTField, ChoiceField, RelatedField, Component, BaseModel, BaseForm, OperandView

class Command(BaseCommand):
    help = 'Import design from json file'

    def handle(self, *args, **options):
        # 删除所有数据
        BoolField.objects.all().delete()
        CharacterField.objects.all().delete()
        NumberField.objects.all().delete()
        DTField.objects.all().delete()
        ChoiceField.objects.all().delete()
        RelatedField.objects.all().delete()
        Component.objects.all().delete()
        BaseModel.objects.all().delete()
        BaseForm.objects.all().delete()
        OperandView.objects.all().delete()        
        
        # 导入数据
        with open('design.json', encoding="utf8") as f:
            design = json.loads(f.read())

        for obj in design:
            model_name = obj['name']
            model_label = obj['label']
            basemodel = BaseModel.objects.create(name=model_name, label=model_label)
            model_components = []
            for field in obj['fields']:
                # _name = "_".join(lazy_pinyin(field['label']))
                if field['model'] == 'CharacterField':
                    if CharacterField.objects.filter(name=field['name']).count() == 0:
                        CharacterField.objects.create(
                            name=field['name'],
                            label=field['label'],
                            type=field['type'],
                        )
                elif field['model'] == 'BoolField':
                    if BoolField.objects.filter(name=field['name']).count() == 0:
                        BoolField.objects.create(
                            name=field['name'],
                            label=field['label'],
                            type=field['type'],
                        )
                elif field['model'] == 'NumberField':
                    if NumberField.objects.filter(name=field['name']).count() == 0:
                        NumberField.objects.create(
                            name=field['name'],
                            label=field['label'],
                            type=field['type'],
                            standard_value=field['standard_value'],
                            up_limit=field['up_limit'],
                            down_limit=field['down_limit'],
                            unit=field['unit'],
                        )
                elif field['model'] == 'DTField':
                    if DTField.objects.filter(name=field['name']).count() == 0:
                        DTField.objects.create(
                            name=field['name'],
                            label=field['label'],
                            type=field['type'],
                        )
                elif field['model'] == 'ChoiceField':
                    if ChoiceField.objects.filter(name=field['name']).count() == 0:
                        ChoiceField.objects.create(
                            name=field['name'],
                            label=field['label'],
                            type=field['type'],
                            options=field['options'],
                        )
                elif field['model'] == 'RelatedField':
                    if RelatedField.objects.filter(name=field['name']).count() == 0:
                        # if field['related_content'] in ['icpc...']:
                        dic, _ = DicList.objects.get_or_create(
                            name=field['related_content'],
                            label=field['related_content_label'],
                            related_field=field['related_field'],
                            content="\n".join(field['dic'])
                        )
                        RelatedField.objects.create(
                            name=field['name'],
                            label=field['label'],
                            type=field['type'],
                            related_content=dic,
                            related_field=field['related_field'],
                        )

                component = Component.objects.get(name=field['name'])
                print(component)
                model_components.append(component)
            
            basemodel.components.set(model_components)
            # basemodel.components.add(*model_components)
            # print(model_components)

            # 创建BaseModel
