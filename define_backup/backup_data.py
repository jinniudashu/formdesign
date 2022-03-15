from django.forms.models import model_to_dict
from time import time
import json

from define.models import *
from define_backup.models import DesignBackup, IcpcBackup
from define_icpc.models import *
from define_operand.models import *
from define_rule_dict.models import *


# 每个需要备份的model都需要在这里添加
# 不备份在其他表新增内容时自动插入内容的表，Component, RelateFieldModel
backup_models = [
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
    EventRule,
    EventExpression,
    IntervalRule,
    FrequencyRule,
    SystemOperand,
    Instruction,
    Service,
    OperationsSetting,
    ServicePackage,
    ServicesSetting,
]


########################################################################################################################
# 设计数据备份
########################################################################################################################
def design_backup(modeladmin, request, queryset):
    design_data = {}

    for model in backup_models:
        _model = model.__name__.lower()
        design_data[_model]=model.objects.backup_data()
        json.dumps(design_data[_model], indent=4, ensure_ascii=False)


    # 写入数据库
    s = DesignBackup.objects.create(
        name = str(int(time())),
        code = json.dumps(design_data, indent=4, ensure_ascii=False),
    )
    print(f'设计数据备份成功, id: {s.id}')

design_backup.short_description = '备份设计数据'


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


# # 一次性导出脚本

# # 字符字段表 26→29
# data=[]
# for item in CharacterField.objects.all():
#     model = model_to_dict(item)
#     if item.name_icpc:
#         model['name_icpc'] = item.name_icpc.icpc_code
#     data.append(model)

# # 关联字段表 42→45
# data=[]
# for item in RelatedField.objects.all():
#     model = model_to_dict(item)
#     model['related_content'] = item.related_content.relate_field_model_id
#     if item.name_icpc:
#         model['name_icpc'] = item.name_icpc.icpc_code
#     data.append(model)

# # 业务表单表 56→58
# data=[]
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
#     model['meta_data'] = None
#     data.append(model)

# # 作业表 24→26
# data=[]
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
#     data.append(model)


# code = json.dumps(data, ensure_ascii=False)