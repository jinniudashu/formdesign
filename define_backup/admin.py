from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
import json
from time import time

from define.models import *
from define_operand.models import *
from define_icpc.models import *
from .models import SourceCode, DesignBackup, IcpcBackup

# 每个需要备份的model都需要在这里添加
# 不备份在其他表新增内容时自动插入内容的表，Component, RelateFieldModel
Backup_models = [
    SystemOperand,
    CycleUnit,
    Role, 
    IcpcList,
    DicList, 
    DicDetail,
    ManagedEntity, 
    CoreModel,
    CharacterField,
    NumberField,
    DTField,
    RelatedField,
    FileField,
    SystemReservedField,
    BuessinessForm,
    FormComponentsSetting,
    FormListComponentsSetting,
    ComputeComponentsSetting,
    ServicePackage,
    Service,
    BuessinessFormsSetting,
    EventRule,
    EventExpression,
    ServicePackageDetail,
    ServiceRule,
    Project,
    ExternalServiceMapping,
    ExternalServiceFieldsMapping,
    Medicine,
]

@admin.register(DesignBackup)
class DesignBackupAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')
    # 增加一个自定义按钮“备份设计数据”
    change_list_template = 'design_backup_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('design_backup/', self.design_backup),
        ]
        return my_urls + urls

    # 备份设计数据
    def design_backup(self, request):
        design_data = {}
        for model in Backup_models:
            _model = model.__name__.lower()
            design_data[_model]=model.objects.backup_data()
            json.dumps(design_data[_model], indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        backup_name = str(int(time()))
        # 写入数据库
        result = DesignBackup.objects.create(
            name = backup_name,
            code = json.dumps(design_data, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder),
        )
        print(f'设计数据备份成功, id: {result}')

        # 写入json文件
        print('开始写入json文件...')
        with open(f'./define_backup/backup/design/design_{backup_name}.json', 'w', encoding='utf-8') as f:
            json.dump(design_data, f, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
            print(f'ICPC写入成功, id: {backup_name}')

        return HttpResponseRedirect("../")


@admin.register(IcpcBackup)
class IcpcBackupAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')
    # 增加一个自定义按钮“备份ICPC”
    change_list_template = 'icpc_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('icpc_backup/', self.icpc_backup),
        ]
        return my_urls + urls

    # 备份ICPC
    def icpc_backup(self, request):
        icpc_data = {}
        for icpc in icpc_list:
            Icpc_model = eval(icpc['name'])
            _key = icpc['name'].lower()
            icpc_data[_key] = Icpc_model.objects.backup_data()

        backup_name = str(int(time()))
        # 写入数据库
        result = IcpcBackup.objects.create(
            name = backup_name,
            code = json.dumps(icpc_data, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder),
        )
        print(f'ICPC数据备份成功, id: {result}')

        # 写入json文件
        print('开始写入json文件...')
        with open(f'./define_backup/backup/icpc/icpc_{backup_name}.json', 'w', encoding='utf-8') as f:
            json.dump(icpc_data, f, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
            print(f'ICPC写入成功, id: {backup_name}')

        return HttpResponseRedirect("../")


@admin.register(SourceCode)
class SourceCodeAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'create_time')
