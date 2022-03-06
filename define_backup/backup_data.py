from django.forms.models import model_to_dict
from time import time
import json

from define.models import *
from define_form.models import *
from define_operand.models import *
from define_backup.models import DesignBackup, IcpcBackup
from define_icpc.models import *

########################################################################################################################
# ICPC数据备份
########################################################################################################################
def icpc_backup(modeladmin, request, queryset):
    icpc_data = {}
    for icpc in icpc_list:
        _key = icpc['name'].lower()
        icpc_data[_key] = []
        Icpc_model = eval(icpc['name'])
        for item in Icpc_model.objects.all():
            _item = model_to_dict(item)
            if _item['pym'] is not None: 
                _item['pym'] = _item['pym'].replace(' ', '')
            icpc_data[_key].append(_item)

    # 写入数据库
    s = IcpcBackup.objects.create(
        name = str(int(time())),
        code = json.dumps(icpc_data, indent=4, ensure_ascii=False),
    )
    print(f'设计数据备份成功, id: {s.id}')

icpc_backup.short_description = '备份ICPC数据'


########################################################################################################################
# 设计数据备份
########################################################################################################################
# 不备份在其他表新增内容时自动插入内容的表，RelateFieldModel
def design_backup(modeladmin, request, queryset):
    # 每个需要备份的model都需要在这里添加
    design_data = {
        'roles': [],
        'managedentities': [],
        'diclists': [],
        'dicdetails': [],
        # 'relatefieldmodels': [],
        'boolfields': [],
        'characterfields': [],
        'numberfields': [],
        'dtfields': [],
        'relatedfields': [],
        'choicefields': [],
        # 'components': [],
        'basemodels': [],
        'baseforms': [],
        'combineforms': [],
        'operations': [],
        'services': [],
        'service_packages': [],
        'instructions': [],
        'events': [],
        'operandintervalrules': [],
        'eventroutes': [],
    }

    for item in Role.objects.all():
        model = model_to_dict(item)
        design_data['roles'].append(model)

    for item in ManagedEntity.objects.all():
        design_data['managedentities'].append(model_to_dict(item))

    for item in DicList.objects.all():
        design_data['diclists'].append(model_to_dict(item))

    for item in DicDetail.objects.all():
        model = model_to_dict(item)
        model['diclist'] = item.diclist.dic_id
        if item.icpc:
            model['icpc'] = item.icpc.icpc_code
        design_data['dicdetails'].append(model)

    for item in BoolField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['boolfields'].append(model)

    for item in CharacterField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['characterfields'].append(model)

    for item in NumberField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['numberfields'].append(model)

    for item in DTField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['dtfields'].append(model)

    for item in RelatedField.objects.all():
        model = model_to_dict(item)
        model['related_content'] = item.related_content.relate_field_model_id
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['relatedfields'].append(model)

    for item in ChoiceField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['choicefields'].append(model)

    # for item in Component.objects.all():
    #     design_data['components'].append(model_to_dict(item))

    for item in BaseModel.objects.all():
        model = model_to_dict(item)

        components = []
        for component in item.components.all():
            components.append(model_to_dict(component))
        model['components'] = components
        
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['managed_entity']:
            managed_entity_name = []
            for managed_entity in model['managed_entity']:
                managed_entity_name.append(managed_entity.entity_id)
            model['managed_entity'] = managed_entity_name

        design_data['basemodels'].append(model)

    # for item in BaseForm.objects.filter(is_inquiry=True):
    for item in BaseForm.objects.all():
        model = model_to_dict(item)

        components = []
        for component in item.components.all():
            components.append(model_to_dict(component))
        model['components'] = components

        model['basemodel'] = item.basemodel.basemodel_id
        model.pop('meta_data')

        design_data['baseforms'].append(model)

    for item in CombineForm.objects.all():
        model = model_to_dict(item)

        forms = []
        for form in item.forms.all():
            _form = model_to_dict(form)
            forms.append(_form['baseform_id'])
        model['forms'] = forms
        
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['managed_entity']:
            model['managed_entity'] = item.managed_entity.entity_id
        model.pop('meta_data')  # 去掉meta_data字段, 因为导入的时候会自动生成

        design_data['combineforms'].append(model)

    for item in Operation.objects.all():
        model = model_to_dict(item)

        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['forms']:
            model['forms'] = item.forms.combineform_id

        if model['group']:
            group_id = []
            for group in item.group.all():
                group_id.append(group.role_id)
            model['group'] = group_id

        design_data['operations'].append(model)


    for item in Service.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['first_operation']:
            model['first_operation'] = item.first_operation.operand_id

        if model['operations']:
            operations_name = []
            for operation in model['operations']:
                operations_name.append(operation.operand_id)
            model['operations'] = operations_name

        if model['group']:
            group_id = []
            for group in item.group.all():
                group_id.append(group.role_id)
            model['group'] = group_id

        design_data['services'].append(model)


    for item in ServicePackage.objects.all():
        model = model_to_dict(item)

        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['first_service']:
            model['first_service'] = item.first_service.service_id

        if model['services']:
            services_id = []
            for service in item.sercices.all():
                services_id.append(service.service_id)
            model['services'] = services_id

        design_data['service_packages'].append(model)


    for item in Instruction.objects.all():
        model = model_to_dict(item)
        design_data['instructions'].append(model)

    for item in Event.objects.all():
        model = model_to_dict(item)
        model['operation'] = item.operation.operand_id
        if model['next_operations']:
            next_operations = []
            for operation in item.next_operations.all():
                next_operations.append(operation.operand_id)
            model['next_operations'] = next_operations
        design_data['events'].append(model)

    for item in OperandIntervalRule.objects.all():
        model = model_to_dict(item)
        model['interval'] = str(item.interval)
        design_data['operandintervalrules'].append(model)

    for item in EventRoute.objects.all():
        model = model_to_dict(item)
        model['event'] = item.event.event_id
        model['operation'] = item.operation.operand_id
        if item.interval_rule:
            model['interval_rule'] = item.interval_rule.operand_interval_rule_id
        design_data['eventroutes'].append(model)

    # 写入数据库
    s = DesignBackup.objects.create(
        name = str(int(time())),
        code = json.dumps(design_data, indent=4, ensure_ascii=False),
    )
    print(f'设计数据备份成功, id: {s.id}')

design_backup.short_description = '备份设计数据'