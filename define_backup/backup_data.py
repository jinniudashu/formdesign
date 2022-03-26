from django.forms.models import model_to_dict
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
Backup_models = [
    Role, 
    ManagedEntity, 
    IcpcList,
    DicList, 
    DicDetail,
    CharacterField,
    NumberField,
    DTField,
    RelatedField,
    ComponentsGroup,
    BuessinessForm,
    FormEntityShip,
    Operation,
    BuessinessFormsSetting,
    EventRule,
    EventExpression,
    Service,
    OperationsSetting,
    ServicePackage,
    ServicePackageDetail,
    ServiceSpec,
    ServiceProgramSetting,
]

def design_backup(modeladmin, request, queryset):
    design_data = {}
    for model in Backup_models:
        _model = model.__name__.lower()
        design_data[_model]=model.objects.backup_data()
        json.dumps(design_data[_model], indent=4, ensure_ascii=False)
    # 写入数据库
    result = write_to_db(DesignBackup, design_data)
    print(f'设计数据备份成功, id: {result}')

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
    result = write_to_db(IcpcBackup, icpc_data)
    print(f'ICPC数据备份成功, id: {result}')

icpc_backup.short_description = '备份ICPC数据'


########################################################################################################################
# 生成作业脚本, 被define_backup.admin调用
########################################################################################################################
def generate_source_code(modeladmin, request, queryset):
    source_code = {}
    
    # 导出字典表models.py, admin.py脚本
    source_code['dict_models'], source_code['dict_admin'] = export_dict_models_admin()
    source_code['dict_data'] = export_dict_data()
    
    # 导出ICPC表models.py, admin.py脚本???
    # source_code['icpc_models'], source_code['icpc_admin'] = IcpcList.export_icpc.models_admin_script()
    # source_code['icpc_data'] = IcpcList.export_icpc.icpc_data()

    # 导出业务表单models.py, admin.py, forms.py脚本
    models_script = models_file_head
    admin_script =  admin_file_head
    forms_script = forms_file_head
    views_script = views_file_head
    urls_script = urls_file_head
    templates_code = []
    index_html_script = index_html_file_head

    for form in BuessinessForm.objects.all():
        if form.script:
            script = json.loads(form.script)
            models_script = f'{models_script}{script["models"]}'
            admin_script = f'{admin_script}{script["admin"]}'
            forms_script = f'{forms_script}{script["forms"]}'
    source_code['models'] = models_script
    source_code['admin'] = admin_script
    source_code['forms'] = forms_script

    # 导出业务表单views.py，template.html, urls.py, index.html脚本
    for service in Service.objects.all():
        if service.script:          
            script = json.loads(service.script)
            views_script = f'{views_script}{script["views"]}'
            urls_script = f'{urls_script}{script["urls"]}'
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

    # 写入数据库
    result = write_to_db(SourceCode, source_code)
    print(f'作业脚本写入数据库成功, id: {result}')

generate_source_code.short_description = '生成作业脚本'


# 导出字典models.py, admin.py脚本
def export_dict_models_admin():
    models_script = dict_models_head
    admin_script = dict_admin_head

    for dict in DicList.objects.all():
        name = dict.name.capitalize()

        # 生成model脚本
        _model_script = f'''
class {name}(DictBase):
class Meta:
verbose_name = '{dict.label}'
verbose_name_plural = verbose_name'''
        models_script = f'{models_script}\n\n{_model_script}'

        # 生成admin脚本
        _admin_script = f'''
@admin.register({name})
class {name}Admin(admin.ModelAdmin):{dict_admin_content}'''
        admin_script = f'{admin_script}\n{_admin_script}'

    return models_script, admin_script


# 导出字典Json数据
def export_dict_data():
    dict_data = []  # 字典明细数据
    for item in DicDetail.objects.all():
        item_dict = model_to_dict(item)
        # 构造字典明细数据
        item_dict['id'] = None
        if item_dict['icpc']:
            item_dict['icpc'] = item.icpc.icpc_code
        item_dict['diclist'] = item.diclist.hssc_id
        dict_data.append(item_dict)

    return dict_data


# 把备份数据写入备份数据库
def write_to_db(model, data):
    s = model.objects.create(
        name = str(int(time())),
        code = json.dumps(data, indent=4, ensure_ascii=False),
    )
    return s.id
