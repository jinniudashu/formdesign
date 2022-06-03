from django.contrib import admin

from .models import BuessinessForm, FormComponentsSetting, Service, BuessinessFormsSetting, ServicePackage, ServicePackageDetail, ServiceSpec, ServiceRule, SystemOperand, EventRule, EventExpression, ManagedEntity


class EventExpressionInline(admin.TabularInline):
    model = EventExpression
    exclude = ['label', 'name', 'hssc_id']
    autocomplete_fields = ['field']

@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'expression', 'detection_scope', 'weight')
    list_display_links = ['label', 'description']
    search_fields=['label', 'name', 'pym']
    readonly_fields = ['hssc_id']
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


class FormComponentsSettingInline(admin.TabularInline):
    model = FormComponentsSetting
    exclude = ['label', 'name', 'hssc_id']
    autocomplete_fields = ['component']

@admin.register(BuessinessForm)
class BuessinessFormAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), 'components_groups', 'description', ('name', 'hssc_id'), )
        }),
    )
    search_fields = ['name', 'label', 'pym']
    filter_horizontal = ("components",)
    readonly_fields = ['name', 'hssc_id']
    inlines = [FormComponentsSettingInline]
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
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority', 'is_system_service'), 'role', 'history_services_display', 'enable_queue_counter', 'route_to', ('awaiting_time_frame' ,'execution_time_frame'), ('name', 'hssc_id'))
        }),
        ('作业管理', {
            'fields': ('suppliers', 'not_suitable', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge', 'generate_script_order')
        }),
    )
    search_fields=['label', 'pym']
    ordering = ['id']
    readonly_fields = ['hssc_id']
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


from django.forms import ModelForm
from define.models import Component
class ManagedEntityAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ManagedEntityAdminForm, self).__init__(*args, **kwargs)
        # 设置管理实体的表头字段范围为当前基础表单字段
        if self.instance.base_form:
            self.fields['header_fields'].queryset = self.instance.base_form.components.all()
        else:
            self.fields['header_fields'].queryset = Component.objects.none()

@admin.register(ManagedEntity)
class ManagedEntityAdmin(admin.ModelAdmin):
    form = ManagedEntityAdminForm
    readonly_fields = ['hssc_id', 'pym', 'name', 'model_name']


# @admin.register(SystemOperand)
# class SystemOperandAdmin(admin.ModelAdmin):
#     list_display = ('id', 'label', 'name', 'func', 'parameters')
#     readonly_fields = ('label','name','hssc_id','func','parameters','description','Applicable','applicable')
#     ordering = ('id',)
