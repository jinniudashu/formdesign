from define_dict.models import DicList
from define_form.models import BaseModel, BaseForm
from define_operand.models import Operation, SourceCode
from time import time
import json

from django.forms.models import model_to_dict
from define.models import BoolField, CharacterField, NumberField, DTField, ChoiceField, RelateFieldModel, RelatedField, Component, ManagedEntity
from define_form.models import CombineForm
from define_operand.models import Service, Event, Instruction, Role, DesignBackup

# 不备份再其他表新增内容时自动插入内容的表，RelateFieldModel
design_data = {
    'roles': [],
    'managedentities': [],
    'diclists': [],
    'boolfields': [],
    'characterfields': [],
    'numberfields': [],
    'dtfields': [],
    'relatedfields': [],
    'choicefields': [],
    'components': [],
    'basemodels': [],
    'baseforms': [],
    'combineforms': [],
    'operations': [],
    'services': [],
    'instructions': [],
    'events': [],
}

for item in Role.objects.all():
    model = model_to_dict(item)
    design_data['roles'].append(model)

for item in ManagedEntity.objects.all():
    design_data['managedentities'].append(model_to_dict(item))

for item in DicList.objects.all():
    design_data['diclists'].append(model_to_dict(item))

for item in BoolField.objects.all():
    design_data['boolfields'].append(model_to_dict(item))

for item in CharacterField.objects.all():
    design_data['characterfields'].append(model_to_dict(item))

for item in NumberField.objects.all():
    design_data['numberfields'].append(model_to_dict(item))

for item in DTField.objects.all():
    design_data['dtfields'].append(model_to_dict(item))

for item in RelatedField.objects.all():
    model = model_to_dict(item)
    related_content_id = model['related_content']
    # related_content_id = model['related_content_new']
    # 获取关联字段值???
    model['related_content'] = DicList.objects.get(id=related_content_id).name
    # model['related_content'] = RelateFieldModel.objects.get(id=related_content_id).name
    design_data['relatedfields'].append(model)

for item in ChoiceField.objects.all():
    design_data['choicefields'].append(model_to_dict(item))

for item in Component.objects.all():
    design_data['components'].append(model_to_dict(item))

for item in BaseModel.objects.all():
    components = []
    for component in item.components.all():
        components.append(model_to_dict(component))
    model = model_to_dict(item)
    model['components'] = components
    design_data['basemodels'].append(model)

for item in BaseForm.objects.filter(is_inquiry=True):
    components = []
    for component in item.components.all():
        components.append(model_to_dict(component))
    model = model_to_dict(item)
    model['components'] = components
    basemodel_id = model['basemodel']
    model['basemodel'] = BaseModel.objects.get(id=basemodel_id).name
    model.pop('meta_data')
    design_data['baseforms'].append(model)

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
    design_data['combineforms'].append(model)

for item in Operation.objects.all():
    model = model_to_dict(item)
    if model['forms']:
        forms_id = model['forms']
        model['forms'] = CombineForm.objects.get(id=forms_id).name
    design_data['operations'].append(model)

for item in Service.objects.all():
    model = model_to_dict(item)
    if model['first_operation']:
        operation_id = model['first_operation']
        model['first_operation'] = Operation.objects.get(id=operation_id).name
    design_data['services'].append(model)

for item in Instruction.objects.all():
    model = model_to_dict(item)
    design_data['instructions'].append(model)

for item in Event.objects.all():
    next_operations = []
    for operation in item.next.all():
        _operation = model_to_dict(operation)
        next_operations.append(_operation['name'])
    model = model_to_dict(item)
    model['next'] = next_operations
    operation_id = model['operation']
    model['operation'] = Operation.objects.get(id=operation_id).name
    design_data['events'].append(model)

# 写入数据库
s = DesignBackup.objects.create(
    name = str(int(time())),
    code = json.dumps(design_data, indent=4, ensure_ascii=False),
)
