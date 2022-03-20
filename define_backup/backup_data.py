from time import time
import json

from define.models import *
from define_icpc.models import *
from define_operand.models import *
from define_rule_dict.models import *
from define_backup.models import DesignBackup, IcpcBackup, SourceCode

from .script_file_header import *

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
    FormEntityShip,
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
    
    # 导出业务表单models.py, admin.py, forms.py脚本
    models_script = models_file_head
    admin_script =  admin_file_head
    forms_script = forms_file_head
    views_script = views_file_head
    urls_script = urls_file_head
    templates_code = []
    index_html_script = index_html_file_head

    for form in BuessinessForm.objects.all():
        script = json.loads(form.script)
        models_script = f"{models_script}{script['models']}"
        admin_script = f"{admin_script}{script['admin']}"
        forms_script = f"{forms_script}{script['forms']}"
    source_code['models'] = models_script
    source_code['admin'] = admin_script
    source_code['forms'] = forms_script

    # 导出业务表单views.py，template.html, urls.py, index.html脚本
    for service in Service.objects.all():                
        script = json.loads(service.script)
        views_script = f"{views_script}{script['views']}"
        urls_script = f"{urls_script}{script['urls']}"
        templates_code.extend(script['templates'])

        # construct index.html script
        ihs = f'''<a class='list-group-item' href='{{% url "{service.first_operation.name}_create_url" %}}'>
{service.first_operation.label}
</a>
'''
        index_html_script = index_html_script + ihs
    templates_code.append({'index.html': f"{index_html_script}'\n</section>\n{{% endblock %}}'"})

    source_code['views'] = views_script
    source_code['urls'] = f'{urls_script}\n]'
    source_code['templates'] = templates_code

    print(source_code['models'])
    print(source_code['admin'])
    print(source_code['forms'])
    print(source_code['views'])
    print(source_code['urls'])
    print(source_code['templates'])
    
    # 写入数据库
    s = SourceCode.objects.create(
        name = str(int(time())),
        code = json.dumps(source_code, ensure_ascii=False),
    )
    print(f'写入数据库成功, id: {s.id}')

generate_source_code.short_description = '生成作业脚本'
