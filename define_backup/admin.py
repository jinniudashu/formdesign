from django.contrib import admin

from .models import *
from .backup_data import design_backup, icpc_backup, export_source_code

@admin.register(DesignBackup)
class DesignBackupAdmin(admin.ModelAdmin):
    actions = [design_backup]


class IcpcBackupAdmin(admin.ModelAdmin):
	actions = [icpc_backup]
admin.site.register(IcpcBackup, IcpcBackupAdmin)


@admin.register(SourceCode)
class SourceCodeAdmin(admin.ModelAdmin):
    actions = [export_source_code]