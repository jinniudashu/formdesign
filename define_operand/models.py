from django.db import models
from django.db.models import Q, F
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, post_delete
import json
import re

from pypinyin import lazy_pinyin
from django.conf import settings

from formdesign.hsscbase_class import HsscBase, HsscPymBase
from define.models import Component, Role, RelateFieldModel, DicList, DicDetail, Medicine
from define_icpc.models import *
from define_operand.utils import generate_js_script, generate_form_event_js_script

# 内核模型定义
class CoreModel(HsscBase):
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="模型名")

    class Meta:
        verbose_name = "内核模型"
        verbose_name_plural = verbose_name

# 在CoreModel保存后自动同步到RelateFieldModel
@receiver(post_save, sender=CoreModel)
def sync_relate_field_model_on_core_model_save(sender, instance, created, **kwargs):
    if created:
        RelateFieldModel.objects.create(
            label=instance.label,
            related_content=instance.model_name,
            related_content_type='core',
            hssc_id=instance.hssc_id
        )
    else:
        RelateFieldModel.objects.filter(hssc_id=instance.hssc_id).update(
            label=instance.label,
            related_content=instance.model_name,
            related_content_type='core',
        )

# 在CoreModel删除后自动同步到RelateFieldModel
@receiver(post_delete, sender=CoreModel)
def sync_relate_field_model_on_core_model_delete(sender, instance, **kwargs):
    RelateFieldModel.objects.filter(hssc_id=instance.hssc_id).delete()


# 管理实体定义
class ManagedEntity(HsscPymBase):
    app_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="所属app名")
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="模型名")
    base_form = models.OneToOneField('BuessinessForm', on_delete=models.SET_NULL, null=True, verbose_name="基础表单")
    header_fields = models.ManyToManyField(Component, blank=True, verbose_name="表头字段")
    header_fields_json = models.JSONField(null=True, blank=True, verbose_name="表头字段json")
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="所属项目")

    class Meta:
        verbose_name = "管理实体"
        verbose_name_plural = verbose_name

# Sync Create and update RelateFieldModel
@receiver(post_save, sender=ManagedEntity, weak=True, dispatch_uid=None)
def relate_field_model_post_save_handler(sender, instance, created, **kwargs):
    if created:
        try:
            RelateFieldModel.objects.create(
                name=instance.name,
                label=instance.label,
                related_content=instance.base_form.name.capitalize(),
                related_content_type='entities',
                hssc_id = instance.hssc_id
            )
        except Exception as e:
            RelateFieldModel.objects.create(
                name=instance.name,
                label=instance.label,
                related_content_type='entities',
                hssc_id = instance.hssc_id
            )
    else:
        if instance.base_form:
            RelateFieldModel.objects.filter(hssc_id=instance.hssc_id).update(
                name=instance.name,
                label=instance.label,
                related_content=instance.base_form.name.capitalize(),
                related_content_type='entities',
            )
        else:
            RelateFieldModel.objects.filter(hssc_id=instance.hssc_id).update(
                name=instance.name,
                label=instance.label,
                related_content_type='entities',
            )

@receiver(m2m_changed, sender=ManagedEntity.header_fields.through)
def header_fields_m2m_changed_handler(sender, instance, action, **kwargs):
    # 对基本表单的表头字段排序，生成header_fields_json
    if 'post' in action:
        header_fields = []
        selected_header_fields = FormComponentsSetting.objects.filter(form=instance.base_form, component__in=instance.header_fields.all()).order_by('position').values('component')
        for item in selected_header_fields:
            field = Component.objects.get(id=item['component'])
            header_fields.append({'name': field.name, 'label': field.label})
        if header_fields == []:
            header_fields = None
        instance.header_fields_json = json.dumps(header_fields)
        instance.save()

class GenerateFormsScriptMixin(object):
    '''
    生成models.py, admin.py, serializers.py 定义脚本
    '''
    # 生成models, admin, forms脚本
    def generate_script(self, domain):
        script = {}
        script['models'], script['admin'], script['serializers'], script['forms'], script['templates'] = self._create_model_script(domain)
        return script

    # generate model and admin script
    def _create_model_script(self, domain):
        # construct model script
        head_script = f'class {self.name.capitalize()}(HsscFormModel):'
        fields_script = ''
        modeladmin_body = {}
        autocomplete_fields = radio_fields = ''

        # !!!待修改：compontents = form.components.all() + form.component_groups.all()
        for form_components in FormComponentsSetting.objects.filter(form=self).order_by('position'):
            component=form_components.component

            # construct fields script
            _script = self._create_model_field_script(component, self)
            
            fields_script = fields_script + _script
            
            # 如果是关联字段，构造ModelAdmin body内容
            if component.content_object.__class__.__name__ == 'RelatedField':
                field_name = component.content_object.name
                # 如果是关联字典，则判断是否单选，如果是单选，是否Radio
                if component.content_object.related_content.related_content_type == 'dictionaries':
                    if component.content_object.__dict__['type'] == 'RadioSelect':
                        radio_fields = radio_fields + f'"{field_name}": admin.VERTICAL, '  # 或admin.HORIZONTAL
                # 否则是关联实体或关联ICPC，需要autocomplete_fields
                else:
                    # construct admin autocomplete_fields script
                    autocomplete_fields = autocomplete_fields + f'"{field_name}", '
        
        if radio_fields:
            modeladmin_body['radio_fields'] = radio_fields
        if autocomplete_fields:
            modeladmin_body['autocomplete_fields'] = autocomplete_fields

        footer_script = self._create_model_footer_script()

        # construct model, admin, serializers script
        model_script = f'{head_script}{fields_script}{footer_script}\n\n'
        admin_script = self._create_admin_script(modeladmin_body)
        serializers_script = self._create_serializers_script()
        forms_script = ''
        return model_script, admin_script, serializers_script, forms_script

    # generate model footer script
    def _create_model_footer_script(self):
        return f'''
    class Meta:
        verbose_name = '{self.label}'
        verbose_name_plural = verbose_name
        '''

    # generate admin script
    def _create_admin_script(self, modeladmin_body_dict):
        modeladmin_body = ''
        if not modeladmin_body_dict:
            modeladmin_body = f'pass'
        else:
            for key, value in modeladmin_body_dict.items():
                if key == 'radio_fields':
                    modeladmin_body = modeladmin_body + f'    {key} = {{{value}}}\n'
                else:
                    modeladmin_body = modeladmin_body + f'    {key} = [{value}]\n'

        name = self.name.capitalize()

        admin_script = f'''
class {name}Admin(admin.ModelAdmin):
    {modeladmin_body}
admin.site.register({name}, {name}Admin)
'''
        return admin_script

    # generate serializers script
    def _create_serializers_script(self):
        name = self.name.capitalize()
        serializers_script = f'''class {name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {name}
        fields = '__all__'
'''
        return serializers_script

    # generate model field script
    def _create_model_field_script(self, component, form, default_value=None, is_list=False):
        script = get_default_instance =''
        field = component.content_object.__dict__
        component_type = component.content_type.__dict__['model']

        # 从表单组件设置中间表中获取is_required属性
        if is_list:
            is_blank = not form.formlistcomponentssetting_set.get(component=component).is_required
        else:
            is_blank = not form.formcomponentssetting_set.get(component=component).is_required

        if component_type == 'characterfield':
            script = self._create_char_field_script(field, is_blank, default_value)
        elif component_type == 'numberfield':
            script = self._create_number_field_script(field, is_blank, default_value)
        elif component_type == 'dtfield':
            script = self._create_datetime_field_script(field, is_blank)
        elif component_type == 'relatedfield':
            if component.content_object.related_content.related_content_type == 'entities':
                field['foreign_key'] = component.content_object.related_content.name.capitalize()
            else:
                field['foreign_key'] = component.content_object.related_content.related_content
            field['foreign_key_type'] = component.content_object.related_content.related_content_type
            script, get_default_instance = self._create_related_field_script(field, is_blank, default_value)
        elif component_type == 'filefield':
            script = self._create_file_field_script(field, is_blank)
        return script, get_default_instance

    # 生成字符型字段定义脚本
    def _create_char_field_script(self, field, is_blank, default_value=None):
        if field['type'] == 'CharField':
            f_type = 'CharField'
        else:
            f_type = 'TextField'

        if default_value:
            f_default = f'default="{default_value}", '
        else:
            f_default = ''

        f_required = f'null=True, blank={str(is_blank)}, '

        return f'''
    {field['name']} = models.{f_type}(max_length={field['length']}, {f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成数字型字段定义脚本
    def _create_number_field_script(self, field, is_blank, default_value=None):
        if field['type'] == 'IntegerField':
            f_type = 'IntegerField'
            f_dicimal = ''
        elif field['type'] == 'DecimalField':
            f_type = 'DecimalField'
            f_dicimal = f'max_digits={field["max_digits"]}, decimal_places={field["decimal_places"]}, '
        else:
            f_type = 'FloatField'
            f_dicimal = ''
        
        # if field['standard_value']:
        #     f_standard_value = f'default={field["standard_value"]}, '
        # else:
        #     f_standard_value = ''
        # if field['up_limit']:
        #     f_up_limit = f'default={field["up_limit"]}, '
        # else:
        #     f_up_limit = ''
        # if field['down_limit']:
        #     f_down_limit = f'default={field["down_limit"]}, '
        # else:
        #     f_down_limit = ''

        if default_value:
            f_default = f'default={default_value}, '
        else:
            f_default = ''

        f_required = f'null=True, blank={str(is_blank)}, '

        return f'''
    {field['name']} = models.{f_type}({f_dicimal}{f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成日期型字段定义脚本
    def _create_datetime_field_script(self, field, is_blank):
        f_default = ''
        if field['type'] == 'DateTimeField':
            f_type = 'DateTimeField'
            if field['default_now']: f_default = 'default=timezone.now(), '
        else:
            f_type = 'DateField'
            if field['default_now']: f_default = 'default=date.today(), '
        
        f_required = f'null=True, blank={str(is_blank)}, '

        return f'''
    {field['name']} = models.{f_type}({f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成关联型字段定义脚本
    def _create_related_field_script(self, field, is_blank, default_value=None):
        related_field_script = ''
        # 构造“设置缺省值”字符串
        f_default = get_default_instance = ''
        if default_value:
            if field['foreign_key_type'] == 'icpc':
                try:
                    default_instance = eval(field['foreign_key']).objects.get(iname=default_value)
                    get_default_instance = f'''
def get_{self.name}_{field["name"]}_instance():
    return {field["foreign_key"]}.objects.get(iname="{default_value}")\n\n'''
                    f_default = f'default=get_{self.name}_{field["name"]}_instance, '
                except:
                    print("缺省值设置错误，没有对应的实例！", self.name, field["name"], default_value)
            elif field['foreign_key_type'] == 'dictionaries':
                try:
                    default_instance = DicDetail.objects.get(value=default_value)
                    get_default_instance = f'''
def get_{self.name}_{field.name}_instance():
    return {field["foreign_key"]}.objects.get(value="{default_value}")\n\n'''
                    f_default = f'default=get_{self.name}_{field.name}_instance, '
                except:
                    print("缺省值设置错误，没有对应的实例！", self.name, field["name"], default_value)
        
        if field['type'] in ['Select', 'RadioSelect']:
            f_required = f'null=True, blank={str(is_blank)}, '
            related_field_script = f'''
    {field['name']} = models.ForeignKey({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', on_delete=models.CASCADE, {f_default}{f_required}verbose_name='{field['label']}')'''
            return related_field_script, get_default_instance

        elif field['type'] in ['SelectMultiple', 'CheckboxSelectMultiple']:
            f_required = f'blank={str(is_blank)}, '
            related_field_script = f'''
    {field['name']} = models.ManyToManyField({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', {f_required}verbose_name='{field['label']}')'''
            return related_field_script, get_default_instance

    # 生成文件型字段定义脚本
    def _create_file_field_script(self, field, is_blank):
        if field['type'] == 'ImageField':
            f_type = 'ImageField'
        else:
            f_type = 'FileField'

        f_required = f'null=True, blank={str(is_blank)}, '

        return f'''
    {field['name']} = models.{f_type}(upload_to='uploads/', {f_required}verbose_name='{field['label']}')'''

# 业务表单定义
class BuessinessForm(GenerateFormsScriptMixin, HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    components = models.ManyToManyField(Component, through='FormComponentsSetting', related_name='components_in_forms', verbose_name="字段")
    list_components = models.ManyToManyField(Component, through='FormListComponentsSetting', related_name='list_components_in_forms', verbose_name="列表字段")
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="表单说明")
    Form_class = [(1, '调查类'), (2, '诊断类'), (3, '治疗类')]
    form_class = models.PositiveSmallIntegerField(choices=Form_class, null=True, verbose_name="表单类型")
    api_fields = models.JSONField(null=True, blank=True, verbose_name="API字段")

    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'

        super().save(*args, **kwargs)

# 业务表单字段设置
class FormComponentsSetting(HsscBase):
    form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name="字段")
    default_value = models.CharField(max_length=255, null=True, blank=True, verbose_name="默认值")
    is_required = models.BooleanField(default=False, verbose_name="是否必填")
    Api_field = [('charge_staff', '责任人'), ('operator', '作业人员'), ('scheduled_time', '计划执行时间')]
    api_field = models.CharField(max_length=50, choices=Api_field, null=True, blank=True, verbose_name="对接系统接口")
    position = models.PositiveSmallIntegerField(default=100, verbose_name="位置顺序")
    show_hint = models.BooleanField(default=False, verbose_name="显示提示")

    class Meta:
        verbose_name = '表单字段设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.form.name) + '_' + str(self.component.name)

# 业务表单列表字段设置
class FormListComponentsSetting(HsscBase):
    form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name="字段")
    default_value = models.CharField(max_length=255, null=True, blank=True, verbose_name="默认值")
    is_required = models.BooleanField(default=False, verbose_name="是否必填")
    position = models.PositiveSmallIntegerField(default=100, verbose_name="位置顺序")
    autofill_fields = models.BooleanField(default=False, verbose_name="自动填充")

    class Meta:
        verbose_name = '表单列表字段设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.form.name) + '_' + str(self.component.name)

# 业务表单计算字段设置
class ComputeComponentsSetting(HsscBase):
    form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    component = models.ForeignKey(Component, on_delete=models.CASCADE, limit_choices_to=Q(formcomponentssetting__form=F('formcomponentssetting__form')), verbose_name="字段")
    description = models.TextField(max_length=512, null=True, blank=True, verbose_name="计算逻辑说明")

    class Meta:
        verbose_name = '计算字段设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.form.name) + '_' + str(self.component.name) + '_计算字段'


class GenerateServiceScriptMixin(GenerateFormsScriptMixin):
    # 是否基本信息表服务
    def _is_base_form_service(self):
        if self.buessiness_forms.all().count()==1 and self.buessiness_forms.all().first() in [entity.base_form for entity in ManagedEntity.objects.all()]:
            return True
        else:
            return False

    # generate model and admin script
    def _create_model_script(self, domain):
        # construct model script
        head_script = f'class {self.name.capitalize()}(HsscFormModel):'
        head_script_list = f'''class {self.name.capitalize()}_list(models.Model):
    {self.name.lower()} = models.ForeignKey({self.name.capitalize()}, on_delete=models.CASCADE, verbose_name='{self.label}')'''
        model_list_script = ''
        admin_script = admin_listInline_script = ''
        fields_script = list_fields_script = header_fields = ''
        modeladmin_body = {}
        fieldssets = autocomplete_fields = radio_fields = search_fields = change_form_template = inlines = list_autocomplete_fields = list_radio_fields = ''
        form_script = ''
        get_default_instances = get_default_list_instances = ''

        computation_logic = []  # 计算字段清单
        service_fields = {}  # 表单字段清单
        form_event_rules = []  # 表单事件规则清单
        generate_params = {'form_event_rules': form_event_rules, 'computed_fields': ''}  # 提示信息清单
        autofill_fields = False  # 是否自动填充关联字段
        show_hint = False  # 是否显示提示信息

        is_base_form = self._is_base_form_service()
        
        if is_base_form:  # 基础信息表
            # admin.py脚本设置
            search_fields = f'"name", "pym", '

            # construct ModelForm script 
            form_script = self._create_base_model_form_script()

        else:  # 属性表
            # 添加表头字段
            fields_script, header_fields = self._construct_header_fields_script()

            # admin.py脚本设置
            fieldssets = f'\n        ("基本信息", {{"fields": (({header_fields}),)}}), '

        for form in self.buessiness_forms.all():
            form_fields = form_list_fields = ''
            for form_components in FormComponentsSetting.objects.filter(form=form).order_by('position'):
                component=form_components.component
                default_value = form_components.default_value
                if form_components.show_hint:
                    show_hint = True

                # 获取服务所有表单字段用户构造表单字段清单
                service_fields[component.name] = component.label
                
                # construct fields script
                _script, _get_default_instance = self._create_model_field_script(component, form, default_value)

                fields_script = fields_script + _script
                get_default_instances = get_default_instances + _get_default_instance
                
                # construct admin body fields script
                form_fields = form_fields + f'"{component.content_object.name}", '

                # 如果是关联字段，构造ModelAdmin body内容
                if component.content_object.__class__.__name__ == 'RelatedField':
                    field_name = component.content_object.name
                    # 如果是关联字典，则判断是否单选，如果是单选，是否Radio
                    if component.content_object.related_content.related_content_type == 'dictionaries':
                        if component.content_object.__dict__['type'] == 'RadioSelect':
                            radio_fields = radio_fields + f'"{field_name}": admin.VERTICAL, '  # 或admin.HORIZONTAL
                    # 否则是关联实体或关联ICPC，需要autocomplete_fields
                    else:
                        # construct admin autocomplete_fields script
                        autocomplete_fields = autocomplete_fields + f'"{field_name}", '
            
            for form_list_components in FormListComponentsSetting.objects.filter(form=form).order_by('position'):
                component=form_list_components.component
                default_value = form_list_components.default_value
                if form_list_components.autofill_fields:
                    autofill_fields = True

                # 获取服务所有表单字段用户构造表单字段清单
                service_fields[component.name] = component.label
                
                # construct fields script
                _script, _get_default_instance = self._create_model_field_script(component, form, default_value, True)

                list_fields_script = list_fields_script + _script
                get_default_list_instances = get_default_list_instances + _get_default_instance
                
                # construct admin body fields script
                # form_list_fields = form_list_fields + f'"{component.content_object.name}", '

                # 如果是关联字段，构造ModelAdmin body内容
                if component.content_object.__class__.__name__ == 'RelatedField':
                    field_name = component.content_object.name
                    # 如果是关联字典，则判断是否单选，如果是单选，是否Radio
                    if component.content_object.related_content.related_content_type == 'dictionaries':
                        if component.content_object.__dict__['type'] == 'RadioSelect':
                            list_radio_fields = list_radio_fields + f'"{field_name}": admin.VERTICAL, '  # 或admin.HORIZONTAL
                    # 否则是关联实体或关联ICPC，需要autocomplete_fields
                    else:
                        # construct admin autocomplete_fields script
                        list_autocomplete_fields = list_autocomplete_fields + f'"{field_name}", '

            # construct admin fieldset script
            fieldssets = fieldssets + f'\n        ("{form.label}", {{"fields": ({form_fields})}}), '

            # construct change_form_template script
            # 判断当前表单是否有计算字段, 如果有生成计算字段清单
            computed_field_items = ComputeComponentsSetting.objects.filter(form=form)
            if computed_field_items.exists():
                # 生成计算字段清单
                for item in computed_field_items:
                    computation_logic.append(item.description)
                # 生成提示信息
                generate_params['computed_fields'] = f'- form definition: {service_fields}\n- computation logic: {computation_logic}'

            # construct model_list script
            if list_fields_script:
                footer_script_list = f'''
    class Meta:
        verbose_name = '{self.label}明细'
        verbose_name_plural = verbose_name
                '''
                model_list_script = f'{get_default_list_instances}{head_script_list}{list_fields_script}{footer_script_list}'

        # 判断当前服务的服务规则中的条件事件是否是表单事件，如果是生成表单事件清单
        service_rules = ServiceRule.objects.filter(service=self, event_rule__event_type="FORM_EVENT")
        if service_rules.exists():
            # 生成表单事件规则清单
            for rule in service_rules:
                form_event_rule = self._extract_dict_info(rule.event_rule.expression)
                form_event_rule['form_event_action'] = rule.system_operand.func
                form_event_rule['detection_scope'] = rule.event_rule.detection_scope
                form_event_rule['form_class_scope'] = rule.event_rule.form_class_scope
                form_event_rules.append(form_event_rule)

        # construct template script        
        template_script = None
        # 设置change_form_template，例如：change_form_template = 'a3101_change_form.html'
        if computation_logic or form_event_rules or autofill_fields or show_hint:
            change_form_template = f'"{self.name.lower()}_change_form.html"'
            # generate custom template JS script
            if (computation_logic):
                template_script = generate_js_script(generate_params)
            if (form_event_rules or autofill_fields or show_hint):
                template_script = generate_form_event_js_script(form_event_rules, domain, self.name.lower(), autofill_fields, show_hint)

        # construct model footer script
        footer_script = self._create_model_footer_script(is_base_form)

        # construct modeladmin body script
        if fieldssets:
            modeladmin_body['fieldssets'] = fieldssets
        if autocomplete_fields:
            modeladmin_body['autocomplete_fields'] = autocomplete_fields
        if radio_fields:
            modeladmin_body['radio_fields'] = radio_fields
        if header_fields:
            modeladmin_body['readonly_fields'] = header_fields
        if search_fields:
            modeladmin_body['search_fields'] = search_fields
        if change_form_template:
            modeladmin_body['change_form_template'] = change_form_template
        if list_fields_script:
            modeladmin_body['inlines'] = f'[{self.name.capitalize()}_listInline, ]'
            admin_listInline_script = f'''
class {self.name.capitalize()}_listInline(admin.TabularInline):
    model = {self.name.capitalize()}_list
    extra = 1
    autocomplete_fields = [{list_autocomplete_fields}]
            '''

        # construct admin script
        admin_script = admin_listInline_script + self._create_admin_script(modeladmin_body)
        # construct serializers script
        serializers_script = self._create_serializers_script()
            
        # construct model script
        model_script = f'{get_default_instances}{head_script}{fields_script}{footer_script}\n{model_list_script}'
        
        return model_script, admin_script, serializers_script, form_script, template_script

    # generate admin script
    def _create_admin_script(self, modeladmin_body_dict):
        modeladmin_body = ''
        if not modeladmin_body_dict:
            modeladmin_body = f'pass'
        else:
            for key, value in modeladmin_body_dict.items():
                if key == 'radio_fields':
                    modeladmin_body = modeladmin_body + f'    {key} = {{{value}}}\n'
                elif key == 'change_form_template':
                    modeladmin_body = modeladmin_body + f'    {key} = {value}\n'
                elif key == 'inlines':
                    modeladmin_body = modeladmin_body + f'    {key} = {value}\n'
                else:
                    modeladmin_body = modeladmin_body + f'    {key} = [{value}]\n'

        name = self.name.capitalize()

        admin_script = f'''
class {name}Admin(HsscFormAdmin):
{modeladmin_body}
admin.site.register({name}, {name}Admin)
clinic_site.register({name}, {name}Admin)
'''
        return admin_script

    # 构建表头字段脚本
    def _construct_header_fields_script(self):
        fields_script = ''
        header_fields = ''

        # 获得按position排序的header_components
        base_form_components = FormComponentsSetting.objects.filter(form=self.managed_entity.base_form).order_by('position')  # 排序的基础信息表字段
        header_components_no_order = self.managed_entity.header_fields.all()  # 没有排序的表头字段
        # 用header_components_no_order从base_form_components中过滤出header_components
        header_components = [component for component in base_form_components if component in header_components_no_order]
        
        for component in header_components:
            # construct fields script
            _script = self._create_model_field_script(component, self.managed_entity.base_form)
            fields_script = fields_script + _script
            header_fields = header_fields + f'"{component.content_object.name}", '
        # 如果服务表单内包含基本信息表，返回空表头字段
        if self.managed_entity.base_form in self.buessiness_forms.all():
            header_fields = ''
        return fields_script, header_fields

    # generate model footer script
    def _create_model_footer_script(self, is_base_form=False):
        footer_script = f'''

    class Meta:
        verbose_name = '{self.label}'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        '''

        base_form_field_pym = f'''
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
        '''
        base_form_footer = f'''
    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name

        '''
        
        if is_base_form:
            return base_form_field_pym + footer_script + base_form_footer
        else:
            return footer_script

    # generate form script
    def _create_base_model_form_script(self):
        service_name = self.name.capitalize()
        # 基础表单字段
        form_component = [fc.component for fc in FormComponentsSetting.objects.filter(form=self.buessiness_forms.all().first()).order_by('position')]
        # 表头字段
        header_component = self.managed_entity.header_fields.all()
        # 按基础表单字段排序的表头字段名
        header_fields = [_component.name for _component in form_component if _component in header_component]
        return f'''
from service.models import {service_name}
class {service_name}_HeaderForm(ModelForm):
    class Meta:
        model = {service_name}
        fields = {header_fields}
        '''

    # 从表达式中提取字典信息
    def _extract_dict_info(self, expression):
        result = {}
        # 使用"and"拆分表达式
        expressions = expression.split(" and ")
        for expr in expressions:
            # 提取字段名部分
            field_name_matches = re.findall(r"\.intersection\((.*?)\)", expr)
            if field_name_matches:
                field_name = field_name_matches[0]

                # 提取字符串集合部分
                sets_matches  = re.findall(r"\{([^}]*)\}", expr)
                if sets_matches:
                    sets = sets_matches[0].split("', '")
                    set_list = [item.strip("'") for item in sets]
                    result[field_name] = set_list

        return result


# 基础作业信息表
class Service(GenerateServiceScriptMixin, HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    buessiness_forms = models.ManyToManyField(BuessinessForm, through='BuessinessFormsSetting', verbose_name="作业表单")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, verbose_name="管理实体")
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    Service_type = [(0, '系统服务'), (1, '管理调度服务'), (2, '诊疗服务')]
    service_type = models.PositiveSmallIntegerField(choices=Service_type, default=2, verbose_name='服务类型')
    role = models.ManyToManyField(Role, blank=True, verbose_name="服务岗位")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    Route_to = [('INDEX', '任务工作台'), ('CUSTOMER_HOMEPAGE', '客户病例首页')]
    route_to = models.CharField(max_length=50, choices=Route_to, default='CUSTOMER_HOMEPAGE', blank=True, null=True, verbose_name='完成跳转至')
    follow_up_required = models.BooleanField(default=False, verbose_name='需要随访')
    follow_up_interval = models.DurationField(blank=True, null=True, verbose_name='随访间隔')
    follow_up_service = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='follow_up_services', verbose_name='随访服务')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')
    generate_script_order = models.PositiveSmallIntegerField(default=100, verbose_name='生成脚本顺序')
    arrange_service_package = models.OneToOneField('ServicePackage', blank=True, null=True, on_delete=models.CASCADE, verbose_name='安排服务包')    
    arrange_service = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='安排服务')    

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


class BuessinessFormsSetting(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="作业")
    buessiness_form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    is_list = models.BooleanField(default=False, verbose_name="列表样式")

    class Meta:
        verbose_name = '服务表单设置'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.buessiness_form)


# 服务包类型信息表
class ServicePackage(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")

    class Meta:
        verbose_name = "服务包"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


class CycleUnit(HsscPymBase):
    cycle_unit = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期单位')
    days = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='天数')
    class Meta:
        verbose_name = "服务周期单位"
        verbose_name_plural = verbose_name

class ServicePackageDetail(HsscPymBase):
    order = models.PositiveSmallIntegerField(default=100, verbose_name='顺序')
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    cycle_unit = models.ForeignKey(CycleUnit, on_delete=models.CASCADE, default=1, blank=True, null=True, verbose_name='周期单位')
    cycle_frequency = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="每周期频次")
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="天数")
    Default_beginning_time = [(0, '指定开始时间'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')]
    default_beginning_time = models.PositiveSmallIntegerField(choices=Default_beginning_time, default=1, verbose_name='执行时间基准')
    base_interval = models.DurationField(blank=True, null=True, verbose_name='基准间隔', help_text='例如：3 days, 22:00:00')

    class Meta:
        verbose_name = "服务内容模板"
        verbose_name_plural = verbose_name
        ordering = ['order']

    def __str__(self):
        return str(self.service)


# 系统作业指令表
class SystemOperand(HsscBase):
    func = models.CharField(max_length=255, blank=True, null=True, verbose_name="内部实现函数")
    parameters = models.CharField(max_length=255, blank=True, null=True, verbose_name="参数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    Operand_type = [('SCHEDULE_OPERAND', '调度作业'), ('FORM_OPERAND', '表单作业')]
    operand_type = models.CharField(max_length=100, choices=Operand_type, default='SCHEDULE_OPERAND', verbose_name="系统作业类型")

    class Meta:
        verbose_name = '系统自动作业'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

# 系统自动作业参数
class SystemOperandParameter(HsscBase):
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="说明")
    parameter1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统参数1")
    form_field1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="对应业务字段1")
    parameter2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统参数2")
    form_field2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="对应业务字段2")
    parameter3 = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统参数3")
    form_field3 = models.CharField(max_length=255, blank=True, null=True, verbose_name="对应业务字段3")

    class Meta:
        verbose_name = '系统自动作业参数'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


# 事件规则表
class EventRule(HsscPymBase):
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="表达式")
    Detection_scope = [('ALL', '所有历史表单'), ('CURRENT_SERVICE', '本次服务表单'), ('LAST_WEEK_SERVICES', '过去7天表单')]
    detection_scope = models.CharField(max_length=100, choices=Detection_scope, default='CURRENT_SERVICE', blank=True, null=True, verbose_name='检测时间范围')
    Form_class = [(0, '所有类型'), (1, '调查类'), (2, '诊断类'), (3, '治疗类')]
    form_class_scope = models.PositiveSmallIntegerField(choices=Form_class, default=0, verbose_name='表单类型范围')
    Event_type = [('FORM_EVENT', '表单事件'), ('SCHEDULE_EVENT', '调度事件')]
    event_type = models.CharField(max_length=100, choices=Event_type, default='SCHEDULE_EVENT', verbose_name="事件类型")
    weight = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="权重")
    expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="内部表达式")
    expression_fields = models.CharField(max_length=1024, blank=True, null=True, verbose_name="内部表达式字段")

    class Meta:
        verbose_name = '条件事件'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    def generate_expression(self):
        # 在EventRuleAdmin.save_formset中调用
        expressions = []
        expression_fields = []
        for _expression in self.eventexpression_set.all():
            field = _expression.field  # 字段

            # 生成子表达式左值, 右值
            left_value = ''
            right_value = ''
            if _expression.char_value:
                value = str(set(_expression.char_value.replace(" ", "").split(',')))
                left_value = f'len({value}.intersection({field.name}))'  # 集合交集判断
                right_value = f'{int(_expression.number_value)}'
            else:
                left_value = f'{field.name}'
                right_value = f'{_expression.number_value}'
            
            # 生成子表达式操作符
            operator = EventExpression.Operator[_expression.operator][1]  # 操作符

            # 生成子表达式and/or连接符
            connection_operator = ''
            if _expression.connection_operator is not None and _expression.connection_operator >= 0:
                connection_operator = EventExpression.Connection_operator[_expression.connection_operator][1]  # 连接符                

            # 组合表达式
            expressions.extend([left_value, operator, right_value, connection_operator])

            # 组合表达式字段
            expression_fields.append(field.name)

        expressions.pop()   # 去掉最后一个连接符
        self.expression = ' '.join(expressions)
        self.expression_fields = ','.join(expression_fields)
        self.save()
        return self.expression

    @staticmethod
    def _is_number(s):
    # 判断传入的字符串是否是数字
        try:
            float(s)
            return True
        except ValueError:
            pass
    
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False


# 事件表达式表
class EventExpression(HsscBase):
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE, null=True, blank=True, verbose_name="事件规则")
    field = models.ForeignKey(Component, on_delete=models.CASCADE, null=True, verbose_name="字段")
    char_value = models.CharField(max_length=255, blank=True, null=True, verbose_name="字符值", help_text="多个值用英文逗号分隔，空格会被忽略")
    Operator = [(0, '=='), (1, '!='), (2, '>'), (3, '<'), (4, '>='), (5, '<=')]
    operator = models.PositiveSmallIntegerField(choices=Operator, null=True, verbose_name='操作符')
    number_value = models.FloatField(blank=True, null=True, verbose_name="数字值")
    Connection_operator = [(0, 'and'), (1, 'or')]
    connection_operator = models.PositiveSmallIntegerField(choices=Connection_operator, blank=True, null=True, verbose_name='连接操作符')
    
    class Meta:
        verbose_name = '事件表达式'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.event_rule.label)


# 服务规则设置
class ServiceRule(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE,  blank=True, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, blank=True, null=True, verbose_name='系统作业')
    next_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='next_service', verbose_name='后续服务')
    Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]  # 接收表单数据
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')
    apply_to_group = models.BooleanField(choices=[(False, '否'), (True, '是')], default=False, verbose_name='应用于分组')
    Complete_feedback = [(0, '否'), (1, '返回完成状态'), (2, '返回表单')]
    complete_feedback = models.PositiveSmallIntegerField(choices=Complete_feedback, default=0,  blank=True, null=True, verbose_name='完成反馈')
    Reminders = [(0, '客户'), (1, '服务人员'), (2, '服务小组')]
    reminders = models.PositiveSmallIntegerField(choices=Reminders, default=0,  blank=True, null=True, verbose_name='提醒对象')
    message = models.CharField(max_length=255, blank=True, null=True, verbose_name='消息内容')
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    interval_rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔条件')
    interval_time = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    is_active = models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')

    class Meta:
        verbose_name = '服务规则'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)


class ExternalServiceMapping(HsscBase):
    external_form_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="外部表单标识")
    external_form_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="外部表单名称")
    Form_source = [('jinshuju', '金数据'), ('other', '其它')]
    form_source = models.CharField(max_length=50, choices=Form_source, null=True, blank=True, verbose_name="来源名称")
    service = models.OneToOneField(Service, on_delete=models.CASCADE, null=True, blank=True, verbose_name="对应服务")
    fields_mapping = models.JSONField(null=True, blank=True, verbose_name="字段映射")

    class Meta:
        verbose_name = '外部服务映射'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.external_form_name)

class ExternalServiceFieldsMapping(HsscBase):
    external_form = models.ForeignKey(ExternalServiceMapping, on_delete=models.CASCADE, null=True, verbose_name="外部表单")
    external_field_name = models.CharField(max_length=100, null=True, verbose_name="外部字段名称")
    service_form_field = models.ForeignKey(Component, on_delete=models.CASCADE, null=True, verbose_name="服务表单字段")

    class Meta:
        verbose_name = '外部服务字段映射'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return str(self.external_field_name)


# 项目定义
class Project(HsscBase):
    domain = models.CharField(max_length=255, null=True, blank=True, verbose_name="域名")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='项目描述')  # 项目描述
    roles = models.ManyToManyField(Role, blank=True, verbose_name='角色')  # 项目角色
    services = models.ManyToManyField(Service, blank=True, verbose_name="服务")
    service_packages = models.ManyToManyField(ServicePackage, blank=True, verbose_name="服务包")
    service_rules = models.ManyToManyField(ServiceRule, blank=True, verbose_name="服务规则")
    external_services = models.ManyToManyField(ExternalServiceMapping, blank=True, verbose_name="外部服务映射")

    class Meta:
        verbose_name = '项目列表'
        verbose_name_plural = verbose_name
        ordering = ['id']
    
    def __str__(self):
        return str(self.label)

    def get_queryset_by_model(self, model_name):
        # 返回project对应model的queryset
        forms_qs = BuessinessForm.objects.filter(service__in=self.services.all())
        if model_name == 'Service':
            return self.services.all()
        elif model_name == 'ManagedEntity':
            return self.managedentity_set.all()
        elif model_name == 'BuessinessForm':
            return BuessinessForm.objects.filter(service__in=self.services.all()).distinct()
        elif model_name == 'BuessinessFormsSetting':
            return BuessinessFormsSetting.objects.filter(service__in=self.services.all()).distinct()
        elif model_name == 'Component':
            return Component.objects.filter(Q(components_in_forms__in=forms_qs) | Q(list_components_in_forms__in=forms_qs)).distinct()
        elif model_name == 'ServicePackage':
            return self.service_packages.all()
        elif model_name == 'ServicePackageDetail':
            return ServicePackageDetail.objects.filter(servicepackage__in=self.service_packages.all()).distinct()
        elif model_name == 'ServiceRule':
            return self.service_rules.all()
        elif model_name == 'EventRule':
            return EventRule.objects.filter(servicerule__in=self.service_rules.all()).distinct()
        elif model_name == 'ExternalServiceMapping':
            return self.external_services.all()
        elif model_name == 'Role':
            return self.roles.all()
        elif model_name == 'DicList':
            return DicList.objects.filter(name__in=[component.content_object.related_content.related_content.lower() for component in Component.objects.filter(Q(components_in_forms__in=forms_qs) | Q(list_components_in_forms__in=forms_qs)).distinct() if component.content_object.__class__.__name__=='RelatedField'])
        
        else:
            # model_name in ['SystemOperand', 'CycleUnit', 'Medicine']
            return eval(model_name).objects.all()
