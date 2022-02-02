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


#######################################
# 以下为测试代码, 备份设计系统数据
#######################################
'''
from define.models import *
from django.forms.models import model_to_dict

data=[]
for item in BoolField.objects.all():
    data.append(model_to_dict(item))

data=[]
for item in CharacterField.objects.all():
    data.append(model_to_dict(item))

data=[]
for item in NumberField.objects.all():
    data.append(model_to_dict(item))

data=[]
for item in DTField.objects.all():
    data.append(model_to_dict(item))

data=[]
for item in RelatedField.objects.all():
    model = model_to_dict(item)
    related_content_id = model['related_content']
    model['related_content'] = DicList.objects.get(id=related_content_id).name
    data.append(model)

data=[]
for item in ChoiceField.objects.all():
    data.append(model_to_dict(item))

data=[]
for item in Component.objects.all():
    data.append(model_to_dict(item))



data=[]
for item in DicList.objects.all():
    data.append(model_to_dict(item))


data=[]
for item in ManagedEntity.objects.all():
    data.append(model_to_dict(item))

data=[]
for item in BaseModel.objects.all():
    components = []
    for component in item.components.all():
        components.append(model_to_dict(component))
    model = model_to_dict(item)
    model['components'] = components
    data.append(model)

data=[]
for item in BaseForm.objects.filter(is_inquiry=True):
    components = []
    for component in item.components.all():
        components.append(model_to_dict(component))
    model = model_to_dict(item)
    model['components'] = components
    basemodel_id = model['basemodel']
    model['basemodel'] = BaseModel.objects.get(id=basemodel_id).name
    model.pop('meta_data')
    data.append(model)

data=[]
for item in CombineForm.objects.filter(is_base=False):
    forms = []
    for form in item.forms.all():
        _form = model_to_dict(form)
        forms.append(_form['name'])
    model = model_to_dict(item)
    model['forms'] = forms
    managed_entity_id = model['managed_entity']
    if managed_entity_id:
        model['managed_entity'] = ManagedEntity.objects.get(id=managed_entity_id).name
    model.pop('meta_data')
    data.append(model)


data=[]
for item in OperandView.objects.all():
    model = model_to_dict(item)
    forms_id = model['forms']
    model['forms'] = CombineForm.objects.get(id=forms_id).name
    data.append(model)

data=[]
for item in SourceCode.objects.all():
    data.append(model_to_dict(item))


with open('design_data_backup.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(design_data, indent=4, ensure_ascii=False))

'''
