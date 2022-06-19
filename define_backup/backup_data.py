from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
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
    FileField,
    ComponentsGroup,
    BuessinessForm,
    FormComponentsSetting,
    Service,
    BuessinessFormsSetting,
    EventRule,
    EventExpression,
    ServicePackage,
    ServicePackageDetail,
    ServiceSpec,
    ServiceRule,
    ExternalServiceMapping,
    ExternalServiceFieldsMapping,
]

def design_backup(modeladmin, request, queryset):
    design_data = {}
    for model in Backup_models:
        _model = model.__name__.lower()
        design_data[_model]=model.objects.backup_data()
        json.dumps(design_data[_model], indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
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
from enum import Enum
def export_source_code(modeladmin, request, queryset):
    source_code = {
        'script': {},
        'data': {}
    }
    
    # 生成脚本的apps
    apps = ['dictionaries','icpc','forms','service']

    forms_query_set = BuessinessForm.objects.all()
    forms_file_header = {
        'models_file_head': forms_models_file_head,
        'admin_file_head': forms_admin_file_head,
        'serializers_head': serializers_head,
    }

    # 基本信息服务排在前面
    service_query_set = Service.objects.filter(is_system_service=False).order_by('-id')
    service_file_header = {
        'models_file_head': service_models_file_head,
        'admin_file_head': service_admin_file_head,
        'serializers_head': serializers_head,
    }
    
    class GetAppScript(Enum):
        dictionaries = get_dict_models_admin_serializers_script()  # 导出App dictionaries: models.py, admin.py脚本
        icpc = get_icpc_models_admin_serializers_script()  # 导出App icpc: models.py, admin.py脚本
        forms = get_models_admin_serializers_script(forms_query_set, forms_file_header)  # 导出App: forms: models.py, admin.py脚本
        service = get_models_admin_serializers_script(service_query_set, service_file_header)  # 导出App:service脚本
        
    for app in apps:
        _script = {}
        _script['models'], _script['admin'], _script['serializers'] = eval(f'GetAppScript.{app}').value
        source_code['script'][app] = _script


    # 导出App:core/hsscbase_class.py脚本
    core = {}
    core['hsscbase_class'] = get_export_hsscbase_class_script('./formdesign/hsscbase_class.py', Component)
    source_code['script']['core'] = core


    # 导出数据
    class GetAppData(Enum):
        dictionaries = get_dict_data  # 导出字典数据json
        icpc = get_icpc_data  # 导出ICPC数据json

    for app in ['dictionaries', 'icpc']:
        source_code['data'][app] = eval(f'GetAppData.{app}')()

    # 导出core业务定义数据：
    # 需要导出的模块清单
    exported_core_models=[
        Role,
        BuessinessForm,
        ManagedEntity,
        Service,
        BuessinessFormsSetting,
        ServicePackage,
        ServicePackageDetail,
        SystemOperand,
        EventRule,
        ServiceSpec,
        ServiceRule,
        ExternalServiceMapping,
    ]
    source_code['data']['core'] = get_init_core_data(exported_core_models)


    # 写入数据库
    result = write_to_db(SourceCode, source_code)
    print(f'作业脚本写入数据库成功, id: {result}')

export_source_code.short_description = '生成作业脚本'

# 导出forms models.py, admin.py, serializers.py脚本
def get_models_admin_serializers_script(query_set, file_header):
    models_script = file_header['models_file_head']
    admin_script =  file_header['admin_file_head']
    serializers_script = file_header['serializers_head']

    for item in query_set:
        script = item.generate_script()  # 生成最新脚本
        models_script = f'{models_script}{script["models"]}'
        admin_script = f'{admin_script}{script["admin"]}'
        serializers_script = f'{serializers_script}{script["serializers"]}'

    return models_script, admin_script, serializers_script

# 导出字典models.py, admin.py脚本
def get_dict_models_admin_serializers_script():
    models_script = dict_models_head
    admin_script = dict_admin_head
    serializers_script = serializers_head

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

        # 生成serializers脚本
        _serializers_script = f'''class {name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {name}
        fields = 'value'
'''
        serializers_script = f'{serializers_script}\n{_serializers_script}'

    return models_script, admin_script, serializers_script

# 导出ICPC字典models.py, admin.py, serializers.py脚本
def get_icpc_models_admin_serializers_script():
    models_script = icpc_models_head
    models_receiver_post_save = models_receiver_post_delete = ''

    # admin.py脚本
    admin_script = icpc_admin_head

    # serializers.py脚本
    serializers_script = serializers_head

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

        # 生成serializers脚本
        _serializers_script = f'''class {icpc['name']}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {icpc['name']}
        fields = 'iname'
'''
        serializers_script = f'{serializers_script}\n{_serializers_script}'

    models_receiver_post_save = models_receiver_post_save + icpc_models_post_save
    models_receiver_post_delete = models_receiver_post_delete + icpc_models_post_delete
    models_script = models_script + models_receiver_post_save + models_receiver_post_delete

    return models_script, admin_script, serializers_script


# 导出基类脚本hsscbase_class.py
def get_export_hsscbase_class_script(hsscbase_class_filename, fields_model: Component):
    def _get_field_type(component):
        _type = component.content_type.model
        if _type == 'characterfield':
            return 'String'
        elif _type == 'numberfield':
            return 'Numbers'
        elif _type == 'dtfield':
            return 'Datetime' if component.content_object.type == 'DateTimeField' else 'Date'
        elif _type == 'relatedfield':
            # 返回关联字段的类型: Model name
            model_name = component.content_object.related_content.related_content
            app_label = component.content_object.related_content.related_content_type
            return f'{app_label}.{model_name}'

    # 生成FieldsType内容
    fields_type_script = f'from enum import Enum\nclass FieldsType(Enum):'
    for component in fields_model.objects.all():
        field_type = _get_field_type(component)
        fields_type_script = f'{fields_type_script}\n    {component.name} = "{field_type}"  # {component.label}'

    # 获取hsscbase_class脚本内容
    with open(hsscbase_class_filename, 'r', encoding="utf8") as f:
        hsscbase_class = f.read()
    
    # 返回合并内容
    return f'{hsscbase_class}\n\n{fields_type_script}'


# 导出字典Json数据
def get_dict_data():
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

# 导出ICPC字典Json数据
def get_icpc_data():
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

# 导出药品基础数据, 被get_init_core_data调用
def get_medicine_data():
    from django.core.exceptions import ObjectDoesNotExist
    medcine_fields_map = {
        'YptyName' : 'boolfield_yao_pin_tong_yong_zi_duan',  # 药品通用名
        'YPName' : 'boolfield_yao_pin_ming_cheng',  # 药品名称
        'Usage' : 'boolfield_fu_yong_pin_ci',  # 用药频次
        'YPCode' : 'boolfield_yao_pin_bian_ma',  # 药品编码
        'Specification' : 'boolfield_yao_pin_gui_ge',  # 药品规格
        'CFDosage' : 'boolfield_chang_yong_chu_fang_liang',  # 常用处方量
        'ybypbm' : 'boolfield_dui_zhao_yi_bao_ming_cheng',  # 对照医保名称
        'gjjbyp' : 'boolfield_dui_zhao_ji_yao_ming_cheng',  # 对照基药名称
        'XS2CF' : 'boolfield_huan_suan_gui_ze',  # 换算规则
        # '' : 'boolfield_yong_yao_zhou_qi',  # 用药疗程
        'CFMeasure' : 'boolfield_chu_fang_ji_liang_dan_wei',  # 处方计量单位
        # '' : 'boolfield_ru_ku_ji_liang_dan_wei',  # 入库计量单位
        'XSMeasure' : 'boolfield_xiao_shou_ji_liang_dan_wei',  # 销售计量单位
        'Type' : 'boolfield_yong_yao_tu_jing',  # 用药途径
        'YPSort' : 'boolfield_yao_pin_fen_lei',  # 药品分类
    }

    medicine_data = []  # 药品明细数据
    for medicine in Medicine.objects.all():
        medicine_dict = model_to_dict(medicine)

        # 构造药品明细数据 new_item
        new_item = {}
        for old_name, new_name in medcine_fields_map.items():
            field_value = medicine_dict.get(old_name)
            # 数据清理：字符串类型去空格
            if isinstance(field_value, str):
                new_item[new_name] = field_value.strip() 
            else:
                new_item[new_name] = field_value

        # 外键字段的数据转换为hssc_id
        forgin_key_fields = {
            'boolfield_chu_fang_ji_liang_dan_wei': 'Yao_pin_dan_wei',
            'boolfield_xiao_shou_ji_liang_dan_wei': 'Yao_pin_dan_wei',
            'boolfield_yong_yao_tu_jing': 'Yong_yao_tu_jing',
            'boolfield_yao_pin_fen_lei': 'Yao_pin_fen_lei',
        }
        for new_name, forgin_key_model in forgin_key_fields.items():
            dic_list = DicList.objects.get(name=forgin_key_model.lower())
            try:
                dic_detail = DicDetail.objects.get(diclist=dic_list, value=new_item[new_name])
                new_item[new_name] = dic_detail.hssc_id
            except ObjectDoesNotExist:
                new_item[new_name] = None

        medicine_data.append(new_item)

    return medicine_data

# 导出core业务定义数据
def get_init_core_data(models):
    models_data = {}
    for model in models:
        _model = model.__name__.lower()
        models_data[_model]=model.objects.backup_data()

    # 导出药品数据
    models_data['yao_pin_ji_ben_xin_xi_biao'] = get_medicine_data()
    return models_data


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
        code = json.dumps(data, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder),
    )
    return s.id

# 写入文件
def write_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)