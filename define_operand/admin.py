from django.contrib import admin

from .models import Service, ServicePackage, Operation, Event, EventRoute, OperandIntervalRule, Instruction, Event_instructions, Role, SourceCode, DesignBackup
from .utils import generate_source_code, design_backup


class EventInline(admin.TabularInline):
    model = Event
    extra = 0

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc', 'priority'), ('forms', 'execute_datetime'), 'group', ('name', 'operand_id'))
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


class EventRouteInline(admin.TabularInline):
    model = Event.next_operations.through
    exclude = ['event_route_id']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
#     change_form_template = "core/templates/change_form.html"
    list_display = ['label', 'operation', 'name', 'id']
    list_display_links = ['label', 'name', 'operation',]
    search_fields = ['name', 'label']
    readonly_fields = ['fields', 'parameters', 'event_id']
    inlines = [EventRouteInline]
    ordering = ['id']


# @admin.register(EventRoute)
# class EventRouteAdmin(admin.ModelAdmin):
#     list_display = ['event', 'operation', 'id']
#     list_display_links = ['event', 'operation',]
#     readonly_fields= ['event_route_id']
#     ordering = ['id']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc', 'priority'), ('execute_datetime', 'first_operation'), ('operations', 'group'), ('name', 'service_id'))
        }),
        ('作业管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    search_fields = ['name', 'label']
    ordering = ['id']
    readonly_fields = ['name', 'service_id']
    autocomplete_fields = ['name_icpc', ]


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name_icpc', 'id']
    list_display_links = ['label', ]
    search_fields = ['label']
    readonly_fields = ['name', 'service_package_id']
    ordering = ['id']


@admin.register(OperandIntervalRule)
class OperandIntervalRuldAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'rule', 'interval', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        (None, {
            'fields': ('label', ('rule', 'interval'), 'description', ('name', 'operand_interval_rule_id'))
        }),
    )
    search_fields = ['name', 'label']
    readonly_fields = ['name', 'operand_interval_rule_id']
    ordering = ['id']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['label', 'id']
    list_display_links = ['label', ]
    search_fields = ['label']
    readonly_fields = ['name', 'role_id']
    ordering = ['id']


@admin.register(DesignBackup)
class DesignBackupAdmin(admin.ModelAdmin):
    actions = [design_backup]


@admin.register(SourceCode)
class SourceCodeAdmin(admin.ModelAdmin):
    actions = [generate_source_code]


# @admin.register(Event_instructions)
# class Event_instructionsAdmin(admin.ModelAdmin):
#     list_display = ['event', 'instruction', 'order', 'params', 'id']
#     list_display_links = ['event', 'instruction', 'order', 'params']
#     search_fields = ['event']
#     ordering = ['id']


# @admin.register(Instruction)
# class InstructionAdmin(admin.ModelAdmin):
#     list_display = ['label', 'name', 'code', 'func', 'description', 'id']
#     list_display_links = ['label', 'name', 'code', 'func']
#     search_fields = ['name']
#     ordering = ['id']
