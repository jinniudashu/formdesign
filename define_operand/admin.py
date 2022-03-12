from django.contrib import admin

from .models import Event, Event_instructions, BuessinessForm, Operation, Service, OperationsSetting, ServicePackage, ServicesSetting, Role, SystemOperand, Instruction


class FormEntityShipInline(admin.TabularInline):
    model = BuessinessForm.managed_entities.through
    exclude = ['form_entity_ship_id']

@admin.register(BuessinessForm)
class BuessinessFormAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), ('components', 'components_groups'), 'description', 'meta_data', ('name', 'hssc_id'))
        }),
    )
    search_fields = ['name', 'label']
    readonly_fields = ['hssc_id', 'meta_data']
    inlines = [FormEntityShipInline]
    autocomplete_fields = ['name_icpc',]


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc'), ('forms', 'priority' ), 'group', ('awaiting_time_frame' ,'execution_time_frame'), ('name', 'operand_id'))
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
    readonly_fields = ['group', 'name', 'operand_id']
    autocomplete_fields = ["name_icpc", ]


class OperationsSettingInline(admin.TabularInline):
    model = OperationsSetting
    exclude = ['operations_setting_id']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority'), ('first_operation', 'last_operation', ), 'group', ('awaiting_time_frame' ,'execution_time_frame'), ('name', 'service_id'))
        }),
        ('界面设置', {
            'fields':('history_services_display', ('enable_recommanded_list', 'enable_queue_counter'), )
        }),
        ('单元服务管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    search_fields = ['name', 'label']
    inlines = [OperationsSettingInline]
    ordering = ['id']
    readonly_fields = ['name', 'service_id']
    autocomplete_fields = ['name_icpc', ]


class ServicesSettingInline(admin.TabularInline):
    model = ServicesSetting
    exclude = ['services_setting_id']

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'id']
    list_display_links = ['label', ]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), ('first_service', 'last_service'), 'duration', ('awaiting_time_frame' ,'execution_time_frame'), ('name', 'service_package_id'))
        }),
    )
    search_fields = ['label']
    readonly_fields = ['name', 'service_package_id']
    inlines = [ServicesSettingInline]
    ordering = ['id']


@admin.register(SystemOperand)
class SystemOperandAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'name', 'func', 'parameters')
    search_fields = ('id', 'name')
    ordering = ('id',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['label', 'id']
    list_display_links = ['label', ]
    search_fields = ['label']
    readonly_fields = ['name', 'hssc_id']
    ordering = ['id']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
#     change_form_template = "core/templates/change_form.html"
    list_display = ['label', 'operation', 'name', 'id']
    list_display_links = ['label', 'name', 'operation',]
    search_fields = ['name', 'label']
    readonly_fields = ['fields', 'parameters', 'event_id']
    ordering = ['id']


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
