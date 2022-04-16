from cProfile import label
from django.forms.models import model_to_dict
from time import time
import json

from define.models import *
from define_icpc.models import *
from define_operand.models import *
from define_backup.models import DesignBackup, IcpcBackup, SourceCode

from .script_file_header import *


########################################################################################################################
# 设计数据备份
########################################################################################################################
# 每个需要备份的model都需要在这里添加
# 不备份在其他表新增内容时自动插入内容的表，Component, RelateFieldModel
Backup_models = [
    Role, 
    IcpcList,
    DicList, 
    DicDetail,
    ManagedEntity, 
    CharacterField,
    NumberField,
    DTField,
    RelatedField,
    ComponentsGroup,
    BuessinessForm,
    Service,
    BuessinessFormsSetting,
    EventRule,
    EventExpression,
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
# 导出作业脚本, 被define_backup.admin调用
########################################################################################################################
def export_source_code(modeladmin, request, queryset):
    source_code = {}
    
    # 导出字典表models.py, admin.py脚本
    source_code['dict_models'], source_code['dict_admin'] = export_dict_models_admin()
    source_code['dict_data'] = export_dict_data()
    
    # 导出ICPC表models.py, admin.py脚本
    source_code['icpc_models'], source_code['icpc_admin'] = export_icpc_models_admin()
    source_code['icpc_data'] = export_icpc_data()

    # 导出业务表单models.py, admin.py, forms.py脚本
    source_code['models'], source_code['admin'], source_code['forms'] = export_forms_models_admin_forms()

    # 导出业务表单views.py，template.html, urls.py, index.html脚本
    source_code['views'], source_code['urls'], source_code['templates'] = export_views_urls_templates()

    # 写入数据库
    result = write_to_db(SourceCode, source_code)
    print(f'作业脚本写入数据库成功, id: {result}')

export_source_code.short_description = '生成作业脚本'


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
class {name}Admin(admin.ModelAdmin):{dict_admin_content}
clinic_site.register({name}, {name}Admin)
'''
        admin_script = f'{admin_script}\n{_admin_script}'

    return models_script, admin_script


# 导出字典Json数据
def export_dict_data():
    dict_data = []  # 字典明细数据
    for item in DicDetail.objects.all():
        # 构造字典明细数据
        dict_item = {}
        dict_item['model'] = 'dictionaries.' + item.diclist.name.capitalize()  # 字典Model名称
        # 构造fields
        item_dict = model_to_dict(item)
        if item_dict['icpc']:
            item_dict['icpc'] = item.icpc.icpc_code
        item_dict.pop('id')
        item_dict.pop('diclist')
        dict_item['fields'] = item_dict

        dict_data.append(dict_item)
    return dict_data


# 导出ICPC字典models.py, admin.py脚本
def export_icpc_models_admin():
    models_script = icpc_models_head
    models_receiver_post_save = models_receiver_post_delete = ''

    # admin.py脚本
    admin_script = icpc_admin_head

    for icpc in icpc_list:
        # 生成model脚本
        _model_script = f'''class {icpc['name']}(IcpcSubBase):
    class Meta:
        verbose_name = '{icpc['label']}'
        verbose_name_plural = verbose_name
'''
        models_script = f'{models_script}\n\n{_model_script}'
        models_receiver_post_save = f'{models_receiver_post_save}\n@receiver(post_save, sender={icpc["name"]}, weak=True, dispatch_uid=None)'
        models_receiver_post_delete = f'{models_receiver_post_delete}\n@receiver(post_delete, sender={icpc["name"]}, weak=True, dispatch_uid=None)'

        # 生成admin脚本
        _admin_script = f'''
admin.site.register({icpc['name']}, SubIcpcAdmin)
clinic_site.register({icpc['name']}, SubIcpcAdmin)'''
        admin_script = f'{admin_script}\n{_admin_script}'

    models_receiver_post_save = models_receiver_post_save + icpc_models_post_save
    models_receiver_post_delete = models_receiver_post_delete + icpc_models_post_delete
    models_script = models_script + models_receiver_post_save + models_receiver_post_delete

    return models_script, admin_script


# 导出ICPC字典Json数据
def export_icpc_data():
    icpc_data = []  # ICPC明细数据
    for icpc in icpc_list:
        icpc_model = eval(icpc['name'])
        # 构造ICPC明细数据
        for _item in icpc_model.objects.all():
            # 构造字典明细数据
            item = {}
            item['model'] = 'icpc.' + icpc['name']  # 字典Model名称
            # 构造fields
            item_dict = model_to_dict(_item)
            item_dict.pop('id')
            item['fields'] = item_dict

            icpc_data.append(item)
    return icpc_data


# 导出forms models.py, admin.py, forms.py脚本
def export_forms_models_admin_forms():
    models_script = models_file_head
    admin_script =  admin_file_head
    forms_script = forms_file_head

    for form in BuessinessForm.objects.all():
        if form.script:
            script = json.loads(form.script)
            models_script = f'{models_script}{script["models"]}'
            admin_script = f'{admin_script}{script["admin"]}'
            forms_script = f'{forms_script}{script["forms"]}'

    return models_script, admin_script, forms_script


# 导出forms views.py, urls.py, templates.py脚本
def export_views_urls_templates():
    views_script = views_file_head
    urls_script = urls_file_head
    templates_code = []
    index_html_script = index_html_file_head

    for service in Service.objects.all():
        if service.script:
            script = json.loads(service.script)
            views_script = f'{views_script}{script["views"]}'
            urls_script = f'{urls_script}{script["urls"]}'
            templates_code.extend(script['templates'])

        # construct index.html script
        index_html_script = index_html_script + generate_index_html(service)
    
    urls_script = f'{urls_script}\n]'
    templates_code.append({'index.html': f"{index_html_script}\n</section>\n{{% endblock %}}"})

    return views_script, urls_script, templates_code


# construct index.html script
def generate_index_html(service):
    return f'''<a class='list-group-item' href='{{% url "{service.name}_create_url" %}}'>
{service.label}
</a>
<hr>
'''


# 把备份数据写入备份数据库
def write_to_db(model, data):
    s = model.objects.create(
        name = str(int(time())),
        code = json.dumps(data, indent=4, ensure_ascii=False),
    )
    return s.id


def write_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)