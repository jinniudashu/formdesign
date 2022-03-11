from django.contrib import admin

from .models import Operation, Event, EventRoute, Service, ServiceOperationsShip, ServicePackage, ServicePackageServicesShip, Role, IntervalRule, EventRule, EventExpression, SystemOperand, FrequencyRule, Instruction, Event_instructions


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


class ServiceOperationsShipInline(admin.TabularInline):
    model = ServiceOperationsShip
    exclude = ['service_operations_ship_id']

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
    inlines = [ServiceOperationsShipInline]
    ordering = ['id']
    readonly_fields = ['name', 'service_id']
    autocomplete_fields = ['name_icpc', ]


class ServicePackageServicesShipInline(admin.TabularInline):
    model = ServicePackageServicesShip
    exclude = ['servicepackage_services_ship_id']

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
    inlines = [ServicePackageServicesShipInline]
    ordering = ['id']


@admin.register(SystemOperand)
class SystemOperandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'func', 'parameters')
    search_fields = ('id', 'name')
    ordering = ('id',)


class EventExpressionInline(admin.TabularInline):
    model = EventExpression
    exclude = ['label', 'name', 'event_expression_id']

@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'expression')
    search_fields = ('id', 'name')
    readonly_fields = ['name', 'event_rule_id']
    inlines = [EventExpressionInline]
    ordering = ('id',)


@admin.register(FrequencyRule)
class FrequencyRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'cycle_option', 'times')
    search_fields = ('id', 'name')
    readonly_fields = ['name', 'frequency_rule_id']
    ordering = ('id',)


@admin.register(IntervalRule)
class IntervalRuldAdmin(admin.ModelAdmin):
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
