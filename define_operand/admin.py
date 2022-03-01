from django.contrib import admin

from .models import Service, ServicePackage, Operation, Event, Instruction, Event_instructions, Role, SourceCode, DesignBackup
from .utils import generate_source_code, design_backup


class EventInline(admin.TabularInline):
    model = Event
    extra = 0

class OperationAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('name_icpc', 'label'), ('forms', 'priority'), 'group', 'name', 'operand_id')
        }),
        ('作业管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    search_fields = ['name', 'label']
    inlines = [EventInline]
    ordering = ['id']
    readonly_fields = ['name', 'operand_id']
    autocomplete_fields = ["name_icpc", ]

admin.site.register(Operation, OperationAdmin)


class EventAdmin(admin.ModelAdmin):
#     change_form_template = "core/templates/change_form.html"
    list_display = ['label', 'name', 'operation', 'id']
    list_display_links = ['label', 'name', 'operation',]
    search_fields = ['name', 'label']
    readonly_fields = ['parameters', 'event_id']
    ordering = ['id']

admin.site.register(Event, EventAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'id']
    list_display_links = ['label', ]
    search_fields = ['label']
    readonly_fields = ['name', 'service_id']
    ordering = ['id']

admin.site.register(Service, ServiceAdmin)


class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name_icpc', 'id']
    list_display_links = ['label', ]
    search_fields = ['label']
    readonly_fields = ['name', 'service_package_id']
    ordering = ['id']

admin.site.register(ServicePackage, ServicePackageAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ['label', 'id']
    list_display_links = ['label', ]
    search_fields = ['label']
    readonly_fields = ['name', 'role_id']
    ordering = ['id']

admin.site.register(Role, RoleAdmin)


class DesignBackupAdmin(admin.ModelAdmin):
    actions = [design_backup]

admin.site.register(DesignBackup, DesignBackupAdmin)


class SourceCodeAdmin(admin.ModelAdmin):
    actions = [generate_source_code]

admin.site.register(SourceCode, SourceCodeAdmin)


# class Event_instructionsAdmin(admin.ModelAdmin):
#     list_display = ['event', 'instruction', 'order', 'params', 'id']
#     list_display_links = ['event', 'instruction', 'order', 'params']
#     search_fields = ['event']
#     ordering = ['id']

# admin.site.register(Event_instructions, Event_instructionsAdmin)


# class InstructionAdmin(admin.ModelAdmin):
#     list_display = ['label', 'name', 'code', 'func', 'description', 'id']
#     list_display_links = ['label', 'name', 'code', 'func']
#     search_fields = ['name']
#     ordering = ['id']

# admin.site.register(Instruction, InstructionAdmin)
