from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from time import time
import json

from define.models import *
from define_operand.models import *
from define_icpc.models import *
from .models import SourceCode
from .script_file_header import *


# 导出作业脚本, 被define_operand.admin调用
def export_source_code(project):
    # 导出forms models.py, admin.py, serializers.py脚本
    def __get_models_admin_serializer_forms_script(query_set):
        file_header = {
            'models_file_head': service_models_file_head,
            'admin_file_head': service_admin_file_head,
            'serializers_head': serializers_head,
            'forms_head': service_forms_file_head,
        }

        models_script = file_header['models_file_head']
        admin_script =  file_header['admin_file_head']
        serializers_script = file_header['serializers_head']
        forms_script = file_header['forms_head']

        for item in query_set:
            script = item.generate_script()  # 生成最新脚本
            models_script = f'{models_script}{script["models"]}'
            admin_script = f'{admin_script}{script["admin"]}'
            serializers_script = f'{serializers_script}{script["serializers"]}'
            forms_script = f'{forms_script}{script["forms"]}'

        return {'models': models_script, 'admin': admin_script, 'serializers': serializers_script, 'forms': forms_script}

    # 导出字典models.py, admin.py脚本
    def __get_dict_models_admin_serializers_script(query_set):
        models_script = dict_models_head
        admin_script = dict_admin_head
        serializers_script = serializers_head
        forms_script = ''

        for dict in query_set:
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

        return {'models': models_script, 'admin': admin_script, 'serializers': serializers_script, 'forms': forms_script}

    # 导出ICPC字典models.py, admin.py, serializers.py脚本
    def __get_icpc_models_admin_serializers_script():
        models_script = icpc_models_head
        models_receiver_post_save = models_receiver_post_delete = ''

        # admin.py脚本
        admin_script = icpc_admin_head

        # serializers.py脚本
        serializers_script = serializers_head

        forms_script = ''

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

        return {'models': models_script, 'admin': admin_script, 'serializers': serializers_script, 'forms': forms_script}

    # 导出基类脚本hsscbase_class.py
    def __get_export_hsscbase_class_script(queryset):
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
        fields_type_script = f'''
from enum import Enum
class FieldsType(Enum):
    # 手工添加CustomerSchedule字段数据类型
    scheduled_time = "Datetime"  # 计划执行时间
    overtime = "Datetime"  # 超期时限
    scheduled_operator = "entities.Stuff"  # 计划执行人员
    service = "core.Service"  # 服务
    priority_operator = "core.VirtualStaff"  # 虚拟职员
    is_assigned = "Boolean"  # 是否已生成任务

    # 自动生成字段数据类型'''

        for component in queryset:
            field_type = _get_field_type(component)
            fields_type_script = f'{fields_type_script}\n    {component.name} = "{field_type}"  # {component.label}'

        # 获取hsscbase_class脚本内容
        with open('./formdesign/hsscbase_class.py', 'r', encoding="utf8") as f:
            hsscbase_class = f.read()
        
        # 返回合并内容
        return {'hsscbase_class': f'{hsscbase_class}\n\n{fields_type_script}'}

    # 导出字典Json数据
    def __get_dict_data(queryset):
        dict_data = []  # 字典明细数据
        for item in DicDetail.objects.filter(diclist__in=queryset):
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
    def __get_icpc_data():
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

    # 导出core业务定义数据
    def __get_init_core_data(project):
        # 需要导出的模块清单
        exported_models=[
            SystemOperand,
            CycleUnit,
            Role,
            BuessinessForm,
            ManagedEntity,
            Service,
            BuessinessFormsSetting,
            ServicePackage,
            ServicePackageDetail,
            EventRule,
            ServiceRule,
            ExternalServiceMapping,
            Medicine,
        ]

        models_data = {}
        for model in exported_models:
            # 获取当前model的项目数据
            queryset = project.get_queryset_by_model(model.__name__)
            # 构造model数据
            models_data[model.__name__.lower()]=model.objects.backup_data(queryset)

        return models_data


    # 导出作业脚本, 生成json数据文件
    source_code = {
        'script': {
            'service': {},
            'dictionaries': {},
            'icpc': {},
            'core': {},
        },
        'data': {
            'dictionaries': [],
            'icpc': [],
            'core': {},
        }
    }

    # 生成apps['service']的脚本，生成服务类型为“用户业务服务”的服务
    project_queryset = project.get_queryset_by_model('Service').filter(service_type=2).order_by('-id')
    source_code['script']['service'] = __get_models_admin_serializer_forms_script(project_queryset)  # 导出App:service脚本

    # 生成apps['dictionaries']的脚本和数据
    project_queryset = project.get_queryset_by_model('DicList')
    source_code['script']['dictionaries'] = __get_dict_models_admin_serializers_script(project_queryset)  # 导出App dictionaries: models.py, admin.py脚本
    source_code['data']['dictionaries'] = __get_dict_data(project_queryset)
    
    # 生成apps['icpc']的脚本和数据
    source_code['script']['icpc'] = __get_icpc_models_admin_serializers_script()  # 导出App icpc: models.py, admin.py脚本
    source_code['data']['icpc'] = __get_icpc_data()

    # 导出App:core/hsscbase_class.py脚本
    project_queryset = project.get_queryset_by_model('Component')
    source_code['script']['core'] = __get_export_hsscbase_class_script(project_queryset)

    # 导出core业务定义数据
    source_code['data']['core'] = __get_init_core_data(project)

    # 生成json
    script_name = str(int(time()))

    # 写入数据库
    result = SourceCode.objects.create(
        project = project,
        name = script_name,
        code = json.dumps(source_code, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder),
    )
    print(f'作业脚本写入数据库成功, id: {result}')

    # 写入json文件
    print('开始写入json文件...')
    with open(f'./define_backup/backup/script/作业系统脚本_{project.name}_{script_name}.json', 'w', encoding='utf-8') as f:
        json.dump(source_code, f, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
        print(f'作业脚本写入成功, id: {script_name}')

