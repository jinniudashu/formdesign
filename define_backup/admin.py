from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import *
from .backup_data import icpc_backup, design_backup


@admin.register(SourceCode)
class SourceCodeAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'create_time')
    # actions = [export_source_code]

    
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

    def design_backup(self, request):
        design_backup()
        return HttpResponseRedirect("../")

@admin.register(IcpcBackup)
class IcpcBackupAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')
    # 增加一个自定义按钮“备份ICPC”
    change_list_template = 'icpc_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('icpc_backup/', self._icpc_backup),
        ]
        return my_urls + urls

    def _icpc_backup(self, request):
        icpc_backup()
        return HttpResponseRedirect("../")
