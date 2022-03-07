from django.contrib import admin

from .models import Operation, Event, EventRoute, Service, ServiceEvent, ServiceEventRoute, ServicePackage, ServicePackageEvent, ServicePackageEventRoute, Role, IntervalRule, Instruction, Event_instructions


class EventInline(admin.TabularInline):
    model = Event
    extra = 0

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc'), ('forms', 'priority' ), 'group', ('name', 'operand_id'))
        }),
        ('作业管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    search_fields = ['name', 'label']
    # inlines = [EventInline]
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

# @admin.register(EventRoute)
# class EventRouteAdmin(admin.ModelAdmin):
#     list_display = ['event', 'operation', 'id']
#     list_display_links = ['event', 'operation',]
#     readonly_fields= ['event_route_id']
#     ordering = ['id']


class ServiceEventInline(admin.TabularInline):
    model = ServiceEvent
    extra = 0

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc', 'priority'), ('first_operation', 'last_operation', ), ('operations', 'group'), ('name', 'service_id'))
        }),
        ('单元服务管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    search_fields = ['name', 'label']
    # inlines = [ServiceEventInline]
    ordering = ['id']
    readonly_fields = ['name', 'service_id']
    autocomplete_fields = ['name_icpc', ]

class ServiceEventRouteInline(admin.TabularInline):
    model = ServiceEvent.next_services.through
    exclude = ['service_event_route_id']

@admin.register(ServiceEvent)
class ServiceEventAdmin(admin.ModelAdmin):
    list_display = ['label', 'service', 'name', 'id']
    list_display_links = ['label', 'name', 'service',]
    search_fields = ['name', 'label']
    readonly_fields = ['service_event_id']
    inlines = [ServiceEventRouteInline]
    ordering = ['id']

# @admin.register(ServiceEventRoute)
# class ServiceEventRouteAdmin(admin.ModelAdmin):
#     list_display = ['event', 'service', 'id']
#     list_display_links = ['event', 'service',]
#     readonly_fields= ['service_event_route_id']
#     ordering = ['id']



@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name_icpc', 'id']
    list_display_links = ['label', ]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), ('first_service', 'last_service', ), 'services', ('name', 'service_package_id'))
        }),
    )
    search_fields = ['label']
    readonly_fields = ['name', 'service_package_id']
    ordering = ['id']

class ServicePackageEventRouteInline(admin.TabularInline):
    model = ServicePackageEvent.next_servicepackages.through
    exclude = ['servicepackage_event_route_id']

@admin.register(ServicePackageEvent)
class ServicePackageEventAdmin(admin.ModelAdmin):
    list_display = ['label', 'servicepackage', 'name', 'id']
    list_display_links = ['label', 'name', 'servicepackage',]
    search_fields = ['name', 'label']
    readonly_fields = ['servicepackage_event_id']
    inlines = [ServicePackageEventRouteInline]
    ordering = ['id']

# @admin.register(ServicePackageEventRoute)
# class ServicePackageEventRouteAdmin(admin.ModelAdmin):
#     list_display = ['event', 'servicepackage', 'id']
#     list_display_links = ['event', 'servicepackage',]
#     readonly_fields= ['servicepackage_event_route_id']
#     ordering = ['id']


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
