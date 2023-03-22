from django.contrib import admin

from .models import *
from define_backup.export_source_code import export_source_code


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'name', 'description', 'hssc_id')
    list_display_links = ('id', 'label')
    fieldsets = (
        (None, {
            'fields': (('label', 'name'), ('description'), 'roles', 'services', 'service_packages', 'service_rules', 'external_services')
        }),
    )
    search_fields = ('name', 'label')
    ordering = ('id',)
    filter_horizontal = ('roles', 'services', 'service_packages', 'service_rules', 'external_services')
    change_form_template = 'project_changeform.html'

    def response_change(self, request, obj):
        # 导出作业脚本
        if '_export_source_code' in request.POST:
            export_source_code(obj)
        return super().response_change(request, obj)

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
#     list_display = ('event_rule', 'field', 'char_value', 'operator', 'number_value', 'connection_operator')
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
            'fields': (('label', 'name_icpc'), 'components_groups', 'description', ('api_fields', 'name', 'hssc_id'), )
        }),
    )
    search_fields = ['name', 'label', 'pym']
    filter_horizontal = ("components",)
    readonly_fields = ['api_fields', 'name', 'hssc_id']
    inlines = [FormComponentsSettingInline]
    autocomplete_fields = ['name_icpc',]

    def save_formset(self, request, form, formset, change):
        # 更新api_fields
        import json
        instances = formset.save()
        if instances:
            form = instances[0].form
            api_fields = [{form_components.api_field: form_components.component.content_object.name} for form_components in FormComponentsSetting.objects.filter(form=form, api_field__isnull=False)]
            if api_fields:
                form.api_fields = json.dumps(api_fields)
            else:
                form.api_fields = None
            form.save()


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
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority', 'service_type'), 'role', 'history_services_display', 'enable_queue_counter', 'route_to', ('working_hours' ,'overtime'), ('name', 'hssc_id'))
        }),
        ('质控管理', {
            'fields': ('follow_up_required', 'follow_up_interval', 'follow_up_service')
        }),
        ('作业管理', {
            'fields': ('suppliers', 'not_suitable', 'cost', 'load_feedback')
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


@admin.register(CycleUnit)
class CycleUnitAdmin(admin.ModelAdmin):
    list_display = ['cycle_unit', 'days',]
    list_display_links = ['cycle_unit', 'days',]
    readonly_fields = ['hssc_id', 'name', 'pym']


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
            'fields': (('label', 'name_icpc'), ('name', 'hssc_id'))
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
    readonly_fields = ['hssc_id', 'pym', 'name', 'model_name', 'header_fields_json']


# @admin.register(SystemOperand)
# class SystemOperandAdmin(admin.ModelAdmin):
#     list_display = ('id', 'label', 'name', 'func', 'parameters')
#     ordering = ('id',)


class ExtenalServiceFieldsMappingInline(admin.TabularInline):
    model = ExternalServiceFieldsMapping
    exclude = ['name', 'label', 'hssc_id']
    autocomplete_fields = ['service_form_field']

@admin.register(ExternalServiceMapping)
class ExternalServiceMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_form_id', 'external_form_name', 'service', 'form_source')
    readonly_fields = ('label','name','hssc_id')
    autocomplete_fields = ['service']
    inlines = [ExtenalServiceFieldsMappingInline]
    ordering = ('id',)

    def save_formset(self, request, form, formset, change):
        # 更新fields_mapping
        import json
        instances = formset.save()
        external_form = instances[0].external_form
        fields_mapping = [{instance.external_field_name: instance.service_form_field.name} for instance in ExternalServiceFieldsMapping.objects.filter(external_form=external_form) if instance.service_form_field and instance.external_field_name]
        print('fields_mapping:', fields_mapping)
        if fields_mapping == []:
            fields_mapping = None
        external_form.fields_mapping = json.dumps(fields_mapping)
        external_form.save()
