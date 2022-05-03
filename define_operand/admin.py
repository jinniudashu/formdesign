from django.contrib import admin

from .models import BuessinessForm, Service, BuessinessFormsSetting, ServicePackage, ServicePackageDetail, ServiceSpec, ServiceRule, SystemOperand, EventRule, EventExpression, ManagedEntity


class EventExpressionInline(admin.TabularInline):
    model = EventExpression
    exclude = ['label', 'name', 'hssc_id']
    autocomplete_fields = ['field']

@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'detection_scope', 'weight')
    list_display_links = ['label', 'description']
    search_fields=['label', 'name', 'pym']
    readonly_fields = ['expression', 'hssc_id']
    inlines = [EventExpressionInline]
    ordering = ('id',)

    # 生成表达式
    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        if instances:
            instances[0].event_rule.generate_expression()


# @admin.register(EventExpression)
# class EventExpressionAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['field']


@admin.register(BuessinessForm)
class BuessinessFormAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), 'components', 'components_groups', 'description', ('name', 'hssc_id'), )
        }),
    )
    search_fields = ['name', 'label', 'pym']
    filter_horizontal = ("components",)
    readonly_fields = ['name', 'hssc_id', 'meta_data']
    autocomplete_fields = ['name_icpc',]


class BuessinessFormsSettingInline(admin.TabularInline):
    model = BuessinessFormsSetting
    exclude = ['name', 'label', 'hssc_id']
    autocomplete_fields = ['buessiness_form']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority'), 'role', ('history_services_display', 'enable_queue_counter'), ('name', 'hssc_id'))
        }),
        ('作业管理', {
            'fields': ('suppliers', 'not_suitable', ('awaiting_time_frame' ,'execution_time_frame'), 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge', 'script')
        }),
    )
    search_fields=['label', 'pym']
    ordering = ['id']
    readonly_fields = ['name', 'hssc_id']
    inlines = [BuessinessFormsSettingInline]
    filter_horizontal = ("role",)
    autocomplete_fields = ["name_icpc"]


class ServicePackageDetailInline(admin.TabularInline):
    model = ServicePackageDetail
    exclude = ['name', 'label', 'hssc_id', 'pym']
    autocomplete_fields = ['service']

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'id']
    list_display_links = ['label', ]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), ('begin_time_setting', 'duration', 'awaiting_time_frame' ,'execution_time_frame'), ('name', 'hssc_id'))
        }),
    )
    search_fields=['label', 'pym']
    readonly_fields = ['name', 'hssc_id']
    inlines = [ServicePackageDetailInline]
    ordering = ['id']


@admin.register(ServiceRule)
class ServiceRuleAdmin(admin.ModelAdmin):
    list_display = ['label', 'service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'complete_feedback', 'is_active']
    list_editable = ['service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'complete_feedback', 'is_active']
    list_display_links = ['label', ]
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['service', 'next_service', 'event_rule']
    ordering = ['id']


@admin.register(ManagedEntity)
class ManagedEntityAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym', 'name', 'model_name']


# @admin.register(SystemOperand)
# class SystemOperandAdmin(admin.ModelAdmin):
#     list_display = ('id', 'label', 'name', 'func', 'parameters')
#     readonly_fields = ('label','name','hssc_id','func','parameters','description','Applicable','applicable')
#     ordering = ('id',)


# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
# #     change_form_template = "core/templates/change_form.html"
#     list_display = ['label', 'operation', 'name', 'id']
#     list_display_links = ['label', 'name', 'operation',]
#     search_fields = ['name', 'label']
#     readonly_fields = ['fields', 'parameters', 'event_id']
#     ordering = ['id']


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