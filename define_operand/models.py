from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from pypinyin import lazy_pinyin

from formdesign.hsscbase_class import HsscBase, HsscPymBase
from define.models import Component, ComponentsGroup, Role, RelateFieldModel
from define_icpc.models import Icpc


# 管理实体定义
class ManagedEntity(HsscPymBase):
    app_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="所属app名")
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="模型名")
    base_form = models.OneToOneField('BuessinessForm', on_delete=models.SET_NULL, null=True, verbose_name="基础表单")
    header_fields = models.ManyToManyField(Component, blank=True, verbose_name="表头字段")

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
                related_content_type=instance.app_name,
                hssc_id = instance.hssc_id
            )
        except Exception as e:
            RelateFieldModel.objects.create(
                name=instance.name,
                label=instance.label,
                related_content_type=instance.app_name,
                hssc_id = instance.hssc_id
            )
    else:
        RelateFieldModel.objects.filter(hssc_id=instance.hssc_id).update(
            name=instance.name,
            label=instance.label,
            related_content=instance.base_form.name.capitalize(),
            related_content_type=instance.app_name,
        )


class GenerateFormsScriptMixin(object):
    '''
    生成models.py, admin.py, serializers.py 定义脚本
    '''
    # 生成models, admin, forms脚本
    def generate_script(self):
        script = {}
        script['models'], script['admin'], script['serializers'] = self._create_model_script()
        return script

    # generate model and admin script
    def _create_model_script(self):
        # construct model script
        head_script = f'class {self.name.capitalize()}(HsscFormModel):'
        fields_script = ''
        modeladmin_body = {}
        autocomplete_fields = radio_fields = ''

        print('GenerateFormsScriptMixin: form', self)
        # !!!待修改：compontents = form.components.all() + form.component_groups.all()
        for component in self.components.all():
            # construct fields script
            print('component0: ', component, 'form0: ', self)
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
        return model_script, admin_script, serializers_script

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
    def _create_model_field_script(self, component, form):
        print('component2: ', component, 'form2: ', form)
        script = ''
        field = component.content_object.__dict__
        component_type = component.content_type.__dict__['model']

        # 从表单组件设置中间表中获取is_required属性
        is_blank = not form.formcomponentssetting_set.get(component=component).is_required

        if component_type == 'characterfield':
            script = self._create_char_field_script(field, is_blank)
        elif component_type == 'numberfield':
            script = self._create_number_field_script(field, is_blank)
        elif component_type == 'dtfield':
            script = self._create_datetime_field_script(field, is_blank)
        elif component_type == 'relatedfield':
            field['foreign_key'] = component.content_object.related_content.related_content
            script = self._create_related_field_script(field, is_blank)
        elif component_type == 'filefield':
            script = self._create_file_field_script(field, is_blank)
        return script

    # 生成字符型字段定义脚本
    def _create_char_field_script(self, field, is_blank):
        if field['type'] == 'CharField':
            f_type = 'CharField'
        else:
            f_type = 'TextField'

        if field['default']:
            f_default = f'default="{field["default"]}", '
        else:
            f_default = ''

        f_required = f'null=True, blank={str(is_blank)}, '

        return f'''
    {field['name']} = models.{f_type}(max_length={field['length']}, {f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成数字型字段定义脚本
    def _create_number_field_script(self, field, is_blank):
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

        if field['default']:
            f_default = f'default={field["default"]}, '
        else:
            f_default = ''

        f_required = f'null=True, blank={str(is_blank)}, '

        return f'''
    {field['name']} = models.{f_type}({f_dicimal}{f_default}{f_required}verbose_name='{field['label']}')'''
    # {field['name']}_standard_value = models.{f_type}({f_dicimal}{f_standard_value}{f_required}verbose_name='{field['label']}标准值')
    # {field['name']}_up_limit = models.{f_type}({f_dicimal}{f_up_limit}{f_required}verbose_name='{field['label']}上限')
    # {field['name']}_down_limit = models.{f_type}({f_dicimal}{f_down_limit}{f_required}verbose_name='{field['label']}下限')'''

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
    def _create_related_field_script(self, field, is_blank):
        if field['type'] in ['Select', 'RadioSelect']:
            f_required = f'null=True, blank={str(is_blank)}, '
            return f'''
    {field['name']} = models.ForeignKey({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', on_delete=models.CASCADE, {f_required}verbose_name='{field['label']}')'''

        elif field['type'] in ['SelectMultiple', 'CheckboxSelectMultiple']:
            f_required = f'blank={str(is_blank)}, '
            return f'''
    {field['name']} = models.ManyToManyField({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', {f_required}verbose_name='{field['label']}')'''

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
    components = models.ManyToManyField(Component, through='FormComponentsSetting', verbose_name="字段")
    components_groups = models.ManyToManyField(ComponentsGroup, blank=True, verbose_name="组件")
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="表单说明")

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

class FormComponentsSetting(HsscBase):
    form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name="字段")
    is_required = models.BooleanField(default=False, verbose_name="是否必填")
    Api_field = [('charge_staff', '责任人'), ('operator', '作业人员'), ('scheduled_time', '计划执行时间')]
    api_field = models.CharField(max_length=50, choices=Api_field, null=True, blank=True, verbose_name="对接系统接口")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="位置顺序")

    class Meta:
        verbose_name = '表单组件设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.form.name) + '_' + str(self.component.name)


class GenerateServiceScriptMixin(GenerateFormsScriptMixin):
    # 是否基本信息表服务
    def _is_base_form_service(self):
        if self.buessiness_forms.all().first() in [entity.base_form for entity in ManagedEntity.objects.all()]:
            return True
        else:
            return False

    # generate model and admin script
    def _create_model_script(self):
        head_script = ''
        fields_script = header_fields = ''
        modeladmin_body = {}
        fieldssets = autocomplete_fields = radio_fields = search_fields = ''

        if self._is_base_form_service():  # 基础信息表
            # construct model script
            head_script = f'class {self.name.capitalize()}(HsscBaseFormModel):'
            # admin.py脚本设置
            search_fields = f'"name", "pym", '
        else:  # 属性表
            # construct model script
            head_script = f'class {self.name.capitalize()}(HsscFormModel):'
            # 添加表头字段
            fields_script, header_fields = self._construct_header_fields_script()
            # admin.py脚本设置
            fieldssets = f'\n        ("基本信息", {{"fields": (({header_fields}),)}}), '

        print('GenerateServiceScriptMixin: service', self)
        for form in self.buessiness_forms.all():
        # !!!待修改：compontents = form.components.all() + form.component_groups.all()
            form_fields = ''
            for component in form.components.all():
                print('component1: ', component, 'form1: ', form)
                # construct fields script
                _script = self._create_model_field_script(component, form)

                fields_script = fields_script + _script
                
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
            
            # construct admin fieldset script
            fieldssets = fieldssets + f'\n        ("{form.label}", {{"fields": ({form_fields})}}), '

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

        # construct admin script
        admin_script = self._create_admin_script(modeladmin_body)
        # construct serializers script
        serializers_script = self._create_serializers_script()

        # construct model script
        footer_script = self._create_model_footer_script()
        model_script = f'{head_script}{fields_script}{footer_script}\n'

        return model_script, admin_script, serializers_script

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
        print('GenerateServiceScriptMixin: service', self)
        for component in self.managed_entity.header_fields.all():
            print('componentHeader: ', component, 'formHeader: ', self.managed_entity.base_form)
            # construct fields script
            _script = self._create_model_field_script(component, self.managed_entity.base_form)
            fields_script = fields_script + _script
            header_fields = header_fields + f'"{component.content_object.name}", '
        # 如果服务表单内包含基本信息表，返回空表头字段
        if self.managed_entity.base_form in self.buessiness_forms.all():
            header_fields = ''
        return fields_script, header_fields

    # generate model footer script
    def _create_model_footer_script(self):
        return f'''

    class Meta:
        verbose_name = '{self.label}'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        '''

# 作业基础信息表
class Service(GenerateServiceScriptMixin, HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    buessiness_forms = models.ManyToManyField(BuessinessForm, through='BuessinessFormsSetting', verbose_name="作业表单")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, verbose_name="管理实体")
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    is_system_service = models.BooleanField(default=False, verbose_name='系统内置服务')
    role = models.ManyToManyField(Role, blank=True, verbose_name="服务岗位")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    Route_to = [('INDEX', '任务工作台'), ('CUSTOMER_HOMEPAGE', '客户病例首页')]
    route_to = models.CharField(max_length=50, choices=Route_to, default='CUSTOMER_HOMEPAGE', blank=True, null=True, verbose_name='完成跳转至')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='完成时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='受理时限', help_text='示例: 1d 2:00:00')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')
    generate_script_order = models.PositiveSmallIntegerField(default=100, verbose_name='生成脚本顺序')

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
    services = models.ManyToManyField(Service, through='ServicePackageDetail', verbose_name="服务项目")
    Begin_time_setting = [(0, '人工指定'), (1, '出生日期')]
    begin_time_setting = models.PositiveSmallIntegerField(choices=Begin_time_setting, default=0, verbose_name='开始时间参考')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')

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

class ServicePackageDetail(HsscPymBase):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    Cycle_options = [(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')]
    cycle_option = models.PositiveSmallIntegerField(choices=Cycle_options, default=0, blank=True, null=True, verbose_name='周期')
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="次数")
    reference_start_tim = models.DurationField(blank=True, null=True, verbose_name="参考起始时间", help_text='例如：3 days, 22:00:00')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    check_awaiting_timeout = models.BooleanField(default=False, verbose_name='检查等待超时')

    class Meta:
        verbose_name = "服务内容模板"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)


# 系统作业指令表
class SystemOperand(HsscBase):
    func = models.CharField(max_length=255, blank=True, null=True, verbose_name="内部实现函数")
    parameters = models.CharField(max_length=255, blank=True, null=True, verbose_name="参数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    Applicable = [(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')]
    applicable = models.PositiveSmallIntegerField(choices=Applicable, default=1, verbose_name='适用范围')

    class Meta:
        verbose_name = '系统自动作业'
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
    detection_scope = models.CharField(max_length=100, choices=Detection_scope, default='CURRENT_SERVICE', blank=True, null=True, verbose_name='检测范围')
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
        descriptions = []
        expression_fields = []
        for _expression in self.eventexpression_set.all():
            field = _expression.field  # 字段
            operator = EventExpression.Operator[_expression.operator][1]  # 操作符
            if ',' in _expression.value:
                value = f"{{{_expression.value}}}"  # 值为集合
            elif self._is_number(_expression.value):
                value = _expression.value  # 值为数字
            else:
                value = f"'{_expression.value}'"  # 值为字符串
            if _expression.connection_operator is not None and _expression.connection_operator >= 0:
                connection_operator = EventExpression.Connection_operator[_expression.connection_operator][1]  # 连接符
            else:
                connection_operator = ''
            expressions.extend([field.name, operator, value, connection_operator])
            descriptions.extend([field.label, operator, value, connection_operator])
            expression_fields.append(field.name)
        expressions.pop()   # 去掉最后一个连接符
        descriptions.pop()  # 去掉最后一个连接符
        self.expression = ' '.join(expressions)
        self.description = ' '.join(descriptions)
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
    Operator = [(0, '=='), (1, '!='), (2, '>'), (3, '<'), (4, '>='), (5, '<='), (6, 'in'), (7, 'not in')]
    operator = models.PositiveSmallIntegerField(choices=Operator, null=True, verbose_name='操作符')
    value = models.CharField(max_length=255, null=True, verbose_name="值", help_text="多个值用英文逗号分隔，空格会被忽略")
    Connection_operator = [(0, 'and'), (1, 'or')]
    connection_operator = models.PositiveSmallIntegerField(choices=Connection_operator, blank=True, null=True, verbose_name='连接操作符')

    class Meta:
        verbose_name = '事件表达式'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.event_rule.label)


# 服务规格设置
class ServiceSpec(HsscBase):
    class Meta:
        verbose_name = "服务规格"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


class ServiceRule(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE,  blank=True, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, limit_choices_to=Q(applicable__in = [1, 3]), blank=True, null=True, verbose_name='系统作业')
    next_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='next_service', verbose_name='后续服务')
    Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]  # 接收表单数据
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')
    Complete_feedback = [(0, '否'), (1, '返回完成状态'), (2, '返回表单')]
    complete_feedback = models.PositiveSmallIntegerField(choices=Complete_feedback, default=0,  blank=True, null=True, verbose_name='完成反馈')
    Reminders = [(0, '客户'), (1, '服务人员'), (2, '服务小组')]
    reminders = models.PositiveSmallIntegerField(choices=Reminders, default=0,  blank=True, null=True, verbose_name='提醒对象')
    message = models.CharField(max_length=255, blank=True, null=True, verbose_name='消息内容')
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    interval_rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔条件')
    interval_time = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    is_active = models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')
    service_spec = models.ForeignKey(ServiceSpec, on_delete=models.CASCADE, null=True, verbose_name='服务规格')

    class Meta:
        verbose_name = '服务规则'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)
