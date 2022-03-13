from django.forms.models import model_to_dict
from time import time
import json

from hsscbase_class import icpc_list
from define.models import *
from define_backup.models import DesignBackup, IcpcBackup
from define_icpc.models import *
from define_operand.models import *
from define_rule_dict.models import *

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
def design_backup(modeladmin, request, queryset):
    # 每个需要备份的model都需要在这里添加
    # 不备份在其他表新增内容时自动插入内容的表，Component, RelateFieldModel
    backup_models = [
        EventRule,
        EventExpression,
        IntervalRule,
        FrequencyRule,
        Role, 
        ManagedEntity, 
        DicList, 
        DicDetail,
        BoolField,
        CharacterField,
        NumberField,
        DTField,
        RelatedField,
        ComponentsGroup,
        BuessinessForm,
        Operation,
        Service,
        OperationsSetting,
        ServicePackage,
        ServicesSetting,
        SystemOperand,
        Instruction,
    ]

    design_data = {}

    for model in backup_models:
        _model = model.__name__.lower()
        design_data[_model]=model.objects.backup_data()
        print('model:', design_data[_model])
        json.dumps(design_data[_model], indent=4, ensure_ascii=False)


    # 写入数据库
    s = DesignBackup.objects.create(
        name = str(int(time())),
        code = json.dumps(design_data, indent=4, ensure_ascii=False),
    )
    print(f'设计数据备份成功, id: {s.id}')

design_backup.short_description = '备份设计数据'


    # for item in Role.objects.all():
    #     model = model_to_dict(item)
    #     design_data['roles'].append(model)

    # for item in ManagedEntity.objects.all():
    #     design_data['managedentities'].append(model_to_dict(item))

    # for item in DicList.objects.all():
    #     design_data['diclists'].append(model_to_dict(item))

    # for item in DicDetail.objects.all():
    #     model = model_to_dict(item)
    #     model['diclist'] = item.diclist.dic_id
    #     if item.icpc:
    #         model['icpc'] = item.icpc.icpc_code
    #     design_data['dicdetails'].append(model)

    # for item in BoolField.objects.all():
    #     model = model_to_dict(item)
    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code
    #     design_data['boolfields'].append(model)

    # for item in CharacterField.objects.all():
    #     model = model_to_dict(item)
    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code
    #     design_data['characterfields'].append(model)

    # for item in NumberField.objects.all():
    #     model = model_to_dict(item)
    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code
    #     design_data['numberfields'].append(model)

    # for item in DTField.objects.all():
    #     model = model_to_dict(item)
    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code
    #     design_data['dtfields'].append(model)

    # for item in RelatedField.objects.all():
    #     model = model_to_dict(item)
    #     model['related_content'] = item.related_content.relate_field_model_id
    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code
    #     design_data['relatedfields'].append(model)

    # for item in ComponentsGroup.objects.all():
    #     model = model_to_dict(item)
    #     components=[]
    #     for component in item.components.all():
    #         components.append(component.field_id)
    #     model['components'] = components
    #     design_data['componentsgroups'].append(model)

    # # for item in BaseModel.objects.all():
    # #     model = model_to_dict(item)
    # #     components = []
    # #     for component in item.components.all():
    # #         components.append(model_to_dict(component))
    # #     model['components'] = components
    # #     if item.name_icpc:
    # #         model['name_icpc'] = item.name_icpc.icpc_code
    # #     if model['managed_entity']:
    # #         managed_entitys = []
    # #         for managed_entity in item.managed_entity.all():
    # #             managed_entitys.append(managed_entity.entity_id)
    # #         model['managed_entity'] = managed_entitys
    # #     design_data['basemodels'].append(model)

    # # for item in BaseForm.objects.all():
    # #     model = model_to_dict(item)
    # #     components = []
    # #     for component in item.components.all():
    # #         components.append(model_to_dict(component))
    # #     model['components'] = components
    # #     model['basemodel'] = item.basemodel.basemodel_id
    # #     model.pop('meta_data')
    # #     design_data['baseforms'].append(model)

    # # for item in CombineForm.objects.all():
    # #     model = model_to_dict(item)
    # #     forms = []
    # #     for form in item.forms.all():
    # #         _form = model_to_dict(form)
    # #         forms.append(_form['baseform_id'])
    # #     model['forms'] = forms
    # #     if item.name_icpc:
    # #         model['name_icpc'] = item.name_icpc.icpc_code
    # #     if model['managed_entity']:
    # #         model['managed_entity'] = item.managed_entity.entity_id
    # #     model.pop('meta_data')  # 去掉meta_data字段, 因为导入的时候会自动生成
    # #     design_data['combineforms'].append(model)


    # for item in BuessinessForm.objects.all():
    #     model = model_to_dict(item)
    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code
    #     components = []
    #     for component in item.components.all():
    #         components.append(component.field_id)
    #     model['components'] = components
    #     if model['components_groups']:
    #         components_groups = []
    #         for components_group in item.components_groups.all():
    #             components_groups.append(components_group.components_group_id)
    #         model['components_groups'] = components_groups
    #     if model['managed_entity']:
    #         managed_entitys = []
    #         for managed_entity in item.managed_entity.all():
    #             managed_entitys.append(managed_entity.entity_id)
    #         model['managed_entity'] = managed_entitys
    #     design_data['buessinessforms'].append(model)


    # for item in Operation.objects.all():
    #     model = model_to_dict(item)

    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code

    #     if model['forms']:
    #         model['forms'] = item.forms.buessiness_form_id

    #     if model['group']:
    #         group_id = []
    #         for group in item.group.all():
    #             group_id.append(group.role_id)
    #         model['group'] = group_id

    #     design_data['operations'].append(model)


    # for item in Service.objects.all():
    #     model = model_to_dict(item)
    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code

    #     if model['first_operation']:
    #         model['first_operation'] = item.first_operation.operand_id

    #     if model['group']:
    #         group_id = []
    #         for group in item.group.all():
    #             group_id.append(group.role_id)
    #         model['group'] = group_id

    #     design_data['services'].append(model)


    # for item in ServicePackage.objects.all():
    #     model = model_to_dict(item)

    #     if item.name_icpc:
    #         model['name_icpc'] = item.name_icpc.icpc_code

    #     if model['first_service']:
    #         model['first_service'] = item.first_service.service_id

    #     if model['services']:
    #         services_id = []
    #         for service in item.services.all():
    #             services_id.append(service.service_id)
    #         model['services'] = services_id

    #     design_data['service_packages'].append(model)


    # for item in Instruction.objects.all():
    #     model = model_to_dict(item)
    #     design_data['instructions'].append(model)

    # for item in Event.objects.all():
    #     model = model_to_dict(item)
    #     model['operation'] = item.operation.operand_id
    #     if model['next_operations']:
    #         next_operations = []
    #         for operation in item.next_operations.all():
    #             next_operations.append(operation.operand_id)
    #         model['next_operations'] = next_operations
    #     design_data['events'].append(model)

    # for item in IntervalRule.objects.all():
    #     model = model_to_dict(item)
    #     model['interval'] = str(item.interval)
    #     design_data['intervalrules'].append(model)

    # for item in FrequencyRule.objects.all():
    #     model = model_to_dict(item)
    #     design_data['frequencyrules'].append(model)

    # for item in EventRule.objects.all():
    #     model = model_to_dict(item)
    #     design_data['buessinessrules'].append(model)

    # for item in SystemOperand.objects.all():
    #     model = model_to_dict(item)
    #     design_data['systemoperands'].append(model)
