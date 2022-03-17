from time import time
import json

from define.models import *
from define_icpc.models import *
from define_operand.models import *
from define_rule_dict.models import *
from define_backup.models import DesignBackup, IcpcBackup, SourceCode


########################################################################################################################
# 设计数据备份
########################################################################################################################
# 每个需要备份的model都需要在这里添加
# 不备份在其他表新增内容时自动插入内容的表，Component, RelateFieldModel
backup_models = [
    Role, 
    ManagedEntity, 
    IcpcList,
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
    Service,
    OperationsSetting,
    ServicePackage,
    ServicesSetting,
]

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
        Icpc_model = eval(icpc['name'])
        _key = icpc['name'].lower()
        icpc_data[_key] = Icpc_model.objects.backup_data()

    # 写入数据库
    s = IcpcBackup.objects.create(
        name = str(int(time())),
        code = json.dumps(icpc_data, indent=4, ensure_ascii=False),
    )
    print(f'ICPC数据备份成功, id: {s.id}')

icpc_backup.short_description = '备份ICPC数据'


########################################################################################################################
# 生成作业脚本, 被define_backup.admin调用
########################################################################################################################
def generate_source_code(modeladmin, request, queryset):
    source_code = {}
    source_code['dicts_models'], source_code['dicts_admin'] = DicList.export_dict.models_admin_script()
    source_code['dicts_data'] = DicDetail.export_dict.dict_data()
    
    source_code['models'] , source_code['admin'] = BuessinessForm.export_buessiness_form.models_admin_script()
    source_code['forms'] =  BuessinessForm.export_buessiness_form.forms_script()
    source_code['views'] , source_code['urls'], source_code['templates'] = BuessinessForm.export_buessiness_form.views_urls_templates_script()

    # 写入数据库
    s = SourceCode.objects.create(
        name = str(int(time())),
        code = json.dumps(source_code, ensure_ascii=False),
    )
    print(f'写入数据库成功, id: {s.id}')

generate_source_code.short_description = '生成作业脚本'
