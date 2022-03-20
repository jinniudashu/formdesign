from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, m2m_changed
import json
import uuid

from pypinyin import lazy_pinyin

from hsscbase_class import HsscBase, HsscPymBase
from define.models import ManagedEntity, Component, ComponentsGroup
from define_icpc.models import Icpc
from define_rule_dict.models import EventRule, FrequencyRule, IntervalRule
from .utils import keyword_search


# 业务表单定义
class BuessinessForm(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    components = models.ManyToManyField(Component, blank=True, verbose_name="字段")
    components_groups = models.ManyToManyField(ComponentsGroup, blank=True, verbose_name="组件")
    managed_entities = models.ManyToManyField(ManagedEntity, through='FormEntityShip', verbose_name="关联实体")
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="表单说明")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="元数据")
    script = models.TextField(blank=True, null=True, verbose_name='运行时脚本', help_text="script['models'] , script['admin'], script['forms']")
    

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'

        # 生成meta_data
        if self.meta_data:
            meta_data = json.loads(self.meta_data)
        else:
            meta_data = {}
        meta_data['name'] = self.name
        meta_data['label'] = self.label
        meta_data['hssc_id'] = str(self.hssc_id)
        # 更新meta_data，类型为dict
        self.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name

    # 生成BuessinessForm的meta_data
    def generate_meta_data(self):
        meta_data = json.loads(self.meta_data)
        meta_data['fields'] = self.generate_components_meta_data(self.components.all())  # 根据components重新生成字段记录
        for components_group in self.components_groups.all():  # 根据components_groups重新生成字段记录
            meta_data['fields'].extend(self.generate_components_meta_data(components_group.components.all()))
        self.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
        self.save()

        # 生成models, admin, forms脚本
        self.script = json.dumps(self.generate_script(), ensure_ascii=False)

    # 生成BuessinessForm的字段的meta_data
    def generate_components_meta_data(self, components):
        fields = []
        for component in components:
            field = {}
            field['name'] = component.name
            field['label'] = component.label
            field['hssc_id'] = component.hssc_id
            _type = component.content_object._meta.object_name
            if _type == 'CharacterField':
                field['type'] = 'string'
            elif _type == 'BoolField':
                field['type'] = 'boolean'
            elif _type == 'NumberField':
                field['type'] = 'number'
            elif _type == 'DTField':
                field['type'] = 'datetime'
            elif _type == 'RelatedField':
                field['type'] = component.content_object.related_content.related_content  # 关联表的Model名称
                # 关联Model所属app名称，待补充!!!
                # related_content_type = component.content_object.related_content.related_content_type
                hssc_app_label = ''
                # if hssc_app_label == 'diclist':  # 字典表
                #     hssc_app_label = 'dictionaries'  # 指向hssc.dictionaries
                # elif hssc_app_label == 'managedentity':  # 实体表
                #     hssc_app_label = component.content_object.related_content.content_object.app_name  # 指向hssc.app_name
                field['app_label'] = hssc_app_label
            fields.append(field)
        return fields

    # 生成models, admin, forms脚本
    def generate_script(self):
        script = {}
        _s = self.__CreateModelScript(self)
        script['models'], script['admin'] = _s.create_script()
        _s = self.__CreateFormScript(self)
        script['forms'] = _s.create_script()
        return script

    class __CreateModelScript:
        def __init__(self, form):
            self.name = form.name
            self.label = form.label
            # !!!待修改：compontents = form.components.all() + form.component_groups.all()
            self.components = form.components.all()

        # generate model and admin script
        def create_script(self):
            # construct model script
            head_script = f'class {self.name.capitalize()}(HsscBuessinessFormBase):'

            fields_script = autocomplete_fields = ''
            for component in self.components:
                # construct fields script
                script = self.__create_model_field_script(component)
                fields_script = fields_script + script
                # construct admin autocomplete_fields script
                if component.content_object.__class__.__name__ == 'RelatedField':
                    autocomplete_fields = autocomplete_fields + f'"{component.content_object.__dict__["name"]}", '

            footer_script = self.__create_model_footer_script()

            # construct model and admin script
            model_script = f'{head_script}{fields_script}{footer_script}\n\n'
            admin_script = self.__create_admin_script(autocomplete_fields)

            return model_script, admin_script

        # generate admin script
        def __create_admin_script(self, autocomplete_fields):
            name = self.name.capitalize()
            if autocomplete_fields != '':
                admin_script = f'''
@admin.register({name})
class {name}Admin(admin.ModelAdmin):
    autocomplete_fields = [{autocomplete_fields}]
    '''
            else:
                admin_script = f'''
admin.site.register({name})
    '''
            return admin_script

        # generate model field script
        def __create_model_field_script(self, component):
            script = ''
            field = component.content_object.__dict__
            component_type = component.content_type.__dict__['model']
            if component_type == 'characterfield':
                script = self.__create_char_field_script(field)
            elif component_type == 'numberfield':
                script = self.__create_number_field_script(field)
            elif component_type == 'dtfield':
                script = self.__create_datetime_field_script(field)
            elif component_type == 'relatedfield':
                field['foreign_key'] = component.content_object.related_content.related_content
                script = self.__create_related_field_script(field)
            return script

        # generate model footer script
        def __create_model_footer_script(self):
            return f'''
        class Meta:
            verbose_name = '{self.label}'
            verbose_name_plural = verbose_name

        def get_absolute_url(self):
            return reverse('{self.name}_detail_url', kwargs={{'slug': self.slug}})

        def get_update_url(self):
            return reverse('{self.name}_update_url', kwargs={{'slug': self.slug}})
            '''

        # 生成字符型字段定义脚本
        def __create_char_field_script(self, field):
            if field['type'] == 'CharField':
                f_type = 'CharField'
            else:
                f_type = 'TextField'

            if field['required']:
                f_required = ''
            else:
                f_required = 'null=True, blank=True, '
            f_required = 'null=True, blank=True, '

            if field['default']:
                f_default = f'default="{field["default"]}", '
            else:
                f_default = ''

            return f'''
        {field['name']} = models.{f_type}(max_length={field['length']}, {f_default}{f_required}verbose_name='{field['label']}')'''

        # 生成数字型字段定义脚本
        def __create_number_field_script(self, field):
            if field['type'] == 'IntegerField':
                f_type = 'IntegerField'
                f_dicimal = ''
            elif field['type'] == 'DecimalField':
                f_type = 'DecimalField'
                f_dicimal = f'max_digits={field["max_digits"]}, decimal_places={field["decimal_places"]}, '
            else:
                f_type = 'FloatField'
                f_dicimal = ''
            
            if field['standard_value']:
                f_standard_value = f'default={field["standard_value"]}, '
            else:
                f_standard_value = ''
            if field['up_limit']:
                f_up_limit = f'default={field["up_limit"]}, '
            else:
                f_up_limit = ''
            if field['down_limit']:
                f_down_limit = f'default={field["down_limit"]}, '
            else:
                f_down_limit = ''

            if field['default']:
                f_default = f'default={field["default"]}, '
            else:
                f_default = ''

            if field['required']:
                f_required = 'null=True, '
            else:
                f_required = 'null=True, blank=True, '
            f_required = 'null=True, blank=True, '

            return f'''
        {field['name']} = models.{f_type}({f_dicimal}{f_default}{f_required}verbose_name='{field['label']}')
        {field['name']}_standard_value = models.{f_type}({f_dicimal}{f_standard_value}{f_required}verbose_name='{field['label']}标准值')
        {field['name']}_up_limit = models.{f_type}({f_dicimal}{f_up_limit}{f_required}verbose_name='{field['label']}上限')
        {field['name']}_down_limit = models.{f_type}({f_dicimal}{f_down_limit}{f_required}verbose_name='{field['label']}下限')'''
        
        # 生成日期型字段定义脚本
        def __create_datetime_field_script(self, field):
            f_default = ''
            if field['type'] == 'DateTimeField':
                f_type = 'DateTimeField'
                if field['default_now']: f_default = 'default=timezone.now(), '
            else:
                f_type = 'DateField'
                if field['default_now']: f_default = 'default=date.today(), '
            
            if field['required']:
                f_required = 'null=True, '
            else:
                f_required = 'null=True, blank=True, '

            return f'''
        {field['name']} = models.{f_type}({f_default}{f_required}verbose_name='{field['label']}')'''

        # 生成关联型字段定义脚本
        def __create_related_field_script(self, field):
            if field['type'] in ['Select', 'RadioSelect']:
                if field['type'] == 'Select':
                    f_type = 'Select'
                else:
                    f_type = 'RadioSelect'
                f_required = 'null=True, blank=True, '

                return f'''
        {field['name']} = models.ForeignKey({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', on_delete=models.CASCADE, {f_required}verbose_name='{field['label']}')'''

            elif field['type'] in ['SelectMultiple', 'CheckboxSelectMultiple']:
                if field['type'] == 'SelectMultiple':
                    f_type = 'SelectMultiple'
                else:
                    f_type = 'CheckboxSelectMultiple'

                return f'''
        {field['name']} = models.ManyToManyField({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', verbose_name='{field['label']}')'''

    class __CreateFormScript:
        def __init__(self, form):
            self.name = form.name.capitalize()
            self.label = form.label
            self.components = form.components.all()
            self.fields = ''
            self.widgets = ''

        def create_script(self):
            for component in self.components:
                field_name = component.content_object.__dict__['name']
                # get fields
                self.fields = self.fields + f'\'{field_name}\', '

                # get widgets
                if component.content_type.__dict__['model']=='relatedfield':
                    field_type = component.content_object.__dict__['type']
                    if field_type == 'Select':
                        self.type = 'Select'
                    elif field_type == 'RadioSelect':
                        self.type = 'RadioSelect'
                    elif field_type == 'CheckboxSelectMultiple':
                        self.type = 'CheckboxSelectMultiple'
                    else:
                        self.type = 'SelectMultiple'
                    self.widgets = self.widgets + f'\'{field_name}\': {self.type}, '

            if self.widgets != '':
                self.widgets = f'widgets = {{{self.widgets}}}'

            # construct form script
            head_script = f'''
    class {self.name}_ModelForm(ModelForm):'''

            body_script = f'''
        class Meta:
            model = {self.name}
            fields = [{self.fields}]
            {self.widgets}
            '''
            return f'{head_script}{body_script}'

# 重新生成字段的meta_data
@receiver(m2m_changed, sender=BuessinessForm.components.through)
def buessiness_form_components_changed_handler(sender, instance, action, reverse, model, pk_set, **kwargs):
    instance.generate_meta_data()

# 重新生成字段的meta_data
@receiver(m2m_changed, sender=BuessinessForm.components_groups.through)
def buessiness_form_components_groups_changed_handler(sender, instance, action, reverse, model, pk_set, **kwargs):
    instance.generate_meta_data()


# 表单和实体关系表
class FormEntityShip(HsscBase):
    entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, verbose_name="关联实体")
    form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="业务表单")
    is_base = models.BooleanField(default=False, verbose_name="基本信息表")

    def __str__(self):
        return str(self.entity) + '--' + str(self.form)

    class Meta:
        verbose_name = '表单和实体关系'
        verbose_name_plural = verbose_name


# 角色表
class Role(HsscBase):
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="角色描述")

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        ordering = ['id']


# # 系统作业指令表
class SystemOperand(HsscBase):
    func = models.CharField(max_length=255, blank=True, null=True, verbose_name="内部实现函数")
    parameters = models.CharField(max_length=255, blank=True, null=True, verbose_name="参数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    Applicable = [(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')]
    applicable = models.PositiveSmallIntegerField(choices=Applicable, default=1, verbose_name='适用范围')

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '系统自动作业'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 作业基础信息表
class Operation(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    buessiness_form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, null=True, blank=True, verbose_name="作业表单")
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')
    Operation_priority = [
        (0, '0级'),
        (1, '紧急'),
        (2, '优先'),
        (3, '一般'),
    ]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    group = models.ManyToManyField(Role, blank=True, verbose_name="作业角色")
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    time_limits = models.DurationField(blank=True, null=True, verbose_name='完成时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name
        ordering = ['id']


# # 单元服务类型信息表
class Service(HsscPymBase):
    name = models.CharField(max_length=255, unique=True, verbose_name="name")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=255, verbose_name="名称")
    first_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='first_operation', blank=True, null=True, verbose_name="起始作业")
    last_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='last_operation', blank=True, null=True, verbose_name="结束作业")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, verbose_name="管理实体")
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')
    Operation_priority = [
        (0, '0级'),
        (1, '紧急'),
        (2, '优先'),
        (3, '一般'),
    ]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    group = models.ManyToManyField(Role, blank=True, verbose_name="服务角色")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_recommanded_list = models.BooleanField(default=True, verbose_name='显示推荐作业')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列计数')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    time_limits = models.DurationField(blank=True, null=True, verbose_name='完成时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')
    script = models.TextField(blank=True, null=True, verbose_name='运行时脚本', help_text="script['views'] , script['urls'], script['templates']")

    class Meta:
        verbose_name = "单元服务"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'

        # 生成views, template, urls 脚本
        print(self)
        self.script = json.dumps(self.generate_script(), ensure_ascii=False)

        super().save(*args, **kwargs)
    
    # 生成运行时脚本的views, urls, templates
    def generate_script(self):
        script = {}
        operation = self.first_operation
        base_info_form = FormEntityShip.objects.get(entity=self.managed_entity, is_base=True).form
        base_form_name = f"{base_info_form.name.capitalize()}'ModelForm'"
        # create views.py, template.html, urls.py, index.html script
        _s = self.__CreateViewScript(operation, base_form_name)
        script['views'], script['urls'], script['templates'] = _s.create_script()
        return script

    # create views.py, template.html, urls.py, index.html script
    class __CreateViewScript:
        def __init__(self, operation, base_form_name):
            self.operand_name = operation.name
            self.operand_label = operation.label
            form_meta_data = json.loads(operation.buessiness_form.meta_data)

            self.model_class_name = operation.buessiness_form.name.capitalize()
            self.create_view_name = f"{self.model_class_name}'CreateView'"
            self.update_view_name = f"{self.model_class_name}'UpdateView'"
            self.edit_template_name = f"{self.operand_name}'_edit.html'"
            self.success_url = '/'
            self.base_form_name = base_form_name
            self.attribute_form_name = f"{self.model_class_name}'ModelForm'"
            self.url = f"{self.operand_name}'_update_url'"

        def create_script(self):
            return self.__construct_view_script(), self.__construct_url_script(), self.__construct_html_script()

        # 构造views脚本
        def __construct_view_script(self):
            # create view
            create_script_head = f'''
class {self.create_view_name}(CreateView):
    model = {self.model_class_name}
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {{}}
'''

            create_script_body = f'''
    def get_context_data(self, **kwargs):
        context = super({self.create_view_name}, self).get_context_data(**kwargs)
        base_form = {self.base_form_name}(instance=self.customer, prefix="base_form")
        if self.request.method == 'POST':
            attribute_form = {self.attribute_form_name}(self.request.POST, prefix="attribute_form")
        else:
            attribute_form = {self.attribute_form_name}(prefix="attribute_form")
        # context
        context['base_form'] = base_form
        context['attribute_form'] = attribute_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super({self.attribute_form_name}, self).form_valid(form)
'''
            return f'{create_script_head}{create_script_body}'

#             # update view
#             update_script_head = f'''
# class {self.update_view_name}(CreateView):
#     model = {self.model_class_name}
#     operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])

#     if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
#         return redirect(reverse('index'))
#     operation_proc.group.set([])  # 设置作业进程所属角色组为空
#     # 构造作业开始消息参数
#     operand_started.send(sender={self.operand_name}_update, operation_proc=operation_proc, ocode='rtr', operator=request.user)

#     customer = operation_proc.customer
#     basic_personal_information = Basic_personal_information.objects.get(customer=customer)
#     context = {{}}
#         '''

#             update_script_body = vs[7] + f'''
#         # inquire_forms''' + vs[0] + f'''
#         # mutate_formsets''' + vs[1] + f'''
#         # mutate_forms
#         if request.method == 'POST':'''+ vs[2] + f'''
#             ''' + vs[6] + vs[5] + f'''
#                 # 构造作业完成消息参数
#                 operand_finished.send(sender={self.operand_name}_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
#                 return redirect(reverse('index'))
#         else:''' + vs[3] + f'''
#         # context''' + vs[4]

#             update_script_foot = f'''
#         context['proc_id'] = kwargs['id']
#         return render(request, '{self.operand_name}_update.html', context)

#         '''

            # s = f'{create_script_head}{create_script_body}{create_script_foot}\n\n{update_script_head}{update_script_body}{update_script_foot}'


        # 构造html脚本
        def __construct_html_script(self):
            _hs = f'''
                        <h5>{self.operand_name}</h5>
                        {{{{ {self.operand_name}.as_p }}}}
                        <hr>'''            
            script_head = f'''{{% extends "base.html" %}}

    {{% load crispy_forms_tags %}}

    {{% block content %}}
    '''

            create_script_body = f'''
        <form action={{% url '{self.operand_name}_create_url' %}} method='POST' enctype='multipart/form-data'> 
            {{% csrf_token %}}
                ''' + _hs

            update_script_body = f'''
        <form action={{% url '{self.operand_name}_update_url' proc_id %}} method='POST' enctype='multipart/form-data'> 
            {{% csrf_token %}}
                ''' + _hs

            script_foot = f'''
            <input type="submit" value="提交" /> 
        </form>

    {{% endblock %}}
    '''

            s_create = f'{script_head}{create_script_body}{script_foot}'
            s_update = f'{script_head}{update_script_body}{script_foot}'
            return [{f'{self.operand_name}_create.html': s_create}, {f'{self.operand_name}_create.html': s_update}]

        # 构造urls脚本
        def __construct_url_script(self):
            return f'''
        path('{self.operand_name}/create', {self.operand_name}_create, name='{self.operand_name}_create_url'),
        path('{self.operand_name}/<int:id>/update', {self.operand_name}_update, name='{self.operand_name}_update_url'),'''


# 接收表单数据
Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]

class OperationsSetting(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='单元服务')
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='operation', null=True, verbose_name='作业')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, limit_choices_to=Q(applicable__in = [0, 3]), blank=True, null=True, verbose_name='系统作业')
    next_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, blank=True, null=True, related_name='next_operation', verbose_name='后续作业')
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0, verbose_name='接收表单')
    interval_rule = models.ForeignKey(IntervalRule, on_delete=models.CASCADE, blank=True, null=True, verbose_name="时间间隔限制")

    def __str__(self):
        return str(self.service) + '--' + str(self.operation)

    class Meta:
        verbose_name = '作业关系设置'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 服务包类型信息表
class ServicePackage(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    first_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='first_service', null=True, verbose_name="起始服务")
    last_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='last_service', blank=True, null=True, verbose_name="结束服务")
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "服务包"
        verbose_name_plural = verbose_name
        ordering = ['id']


class ServicesSetting(HsscBase):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='单元服务')
    frequency_rule = models.ForeignKey(FrequencyRule, on_delete=models.CASCADE, null=True, verbose_name='频度')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE,  blank=True, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, limit_choices_to=Q(applicable__in = [1, 3]), blank=True, null=True, verbose_name='系统作业')
    next_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='next_service', verbose_name='后续服务')
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')
    Complete_feedback = [(0, '否'), (1, '返回完成状态'), (2, '返回表单')]
    complete_feedback = models.PositiveSmallIntegerField(choices=Complete_feedback, default=0,  blank=True, null=True, verbose_name='完成反馈')
    Reminders = [(0, '客户'), (1, '服务人员'), (2, '服务小组')]
    reminders = models.PositiveSmallIntegerField(choices=Reminders, default=0,  blank=True, null=True, verbose_name='提醒对象')
    message_content = models.CharField(max_length=255, blank=True, null=True, verbose_name='消息内容')
    check_awaiting_timeout = models.BooleanField(default=False, verbose_name='检查等待超时')
    check_execution_timeout = models.BooleanField(default=False, verbose_name='检查执行超时')
    interval_rule = models.ForeignKey(IntervalRule, on_delete=models.CASCADE, blank=True, null=True, verbose_name="服务时间间隔")

    def __str__(self):
        return str(self.servicepackage) + '--' + str(self.service)

    class Meta:
        verbose_name = '服务关系设置'
        verbose_name_plural = verbose_name
        ordering = ['id']


#**********************************************************************************************************************
# 待清理代码，暂时保留供参考
#**********************************************************************************************************************

# 作业事件表
# # 默认事件：xx作业完成--系统作业名+"_operation_completed"
class Event(models.Model):
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="name")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='from_oid', verbose_name="所属作业")
    expression = models.TextField(max_length=1024, blank=True, null=True, default='completed', verbose_name="规则", 
        help_text='''
        说明：<br>
        1. 作业完成事件: completed<br>
        2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>
        3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"
        ''')
    next_operations = models.ManyToManyField(Operation, verbose_name="后续作业")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="事件描述")
    parameters = models.CharField(max_length=1024, blank=True, null=True, verbose_name="检查字段")
    fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="可用字段")
    event_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="作业事件ID")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.event_id is None:
            self.event_id = uuid.uuid1()

        # 自动为事件名加作业名为前缀
        if self.operation.name not in self.name:
            self.name = f'{self.operation.name}_{self.name}'
            # 保留字：作业完成事件，自动填充expression为'completed'
            if self.name == f'{self.operation.name}_completed':
                self.expression = 'completed'

        if self.operation.form:
            form = json.loads(self.operation.form.meta_data)
            fields = []
            field_names = []
            form_name = form['name']
            for _field in form['fields']:
                field_name = form_name + '-' + _field['name']
                field_label = _field['label']
                field_type = _field['type']
                field_id = _field['hssc_id']
                field_names.append(field_name)
                fields.append(str((field_name, field_label, field_type, field_id)))

            self.fields = '\n'.join(fields)

            # 生成表达式参数列表
            if self.expression and self.expression != 'completed':
                _form_fields = keyword_search(self.expression, field_names)
                self.parameters = ', '.join(_form_fields)

        super().save(*args, **kwargs)


# 指令表
class Instruction(HsscBase):
    code = models.CharField(max_length=10, verbose_name="指令代码")
    func = models.CharField(max_length=100, verbose_name="操作函数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="指令描述")

    class Meta:
        verbose_name = "指令"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 作业事件指令程序表
class Event_instructions(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True, verbose_name="事件")
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, verbose_name="指令")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="指令序号")
    params = models.CharField(max_length=255, blank=True, null=True, verbose_name="创建作业")

    def __str__(self):
        return self.instruction.name

    class Meta:
        verbose_name = "作业事件指令集"
        verbose_name_plural = verbose_name
        ordering = ['event', 'order']


# ********************
# 作业进程设置
# ********************
# 监视事件路由表EventRoute变更，变更事件后续作业时，同步变更事件指令表Event_instructions的内容
# @receiver(post_save, sender=EventRoute)
# def event_route_post_save_handler(sender, instance, created, **kwargs):
#     if created:
#         # 设定指令为 create_operation_proc
#         instruction_create_operation_proc = Instruction.objects.get(name='create_operation_proc')
#         Event_instructions.objects.create(
#             event=instance.event,
#             instruction=instruction_create_operation_proc,
#             params=instance.operation.name,    # 用后续作业name作为指令参数
#         )

# @receiver(post_delete, sender=EventRoute)
# def event_route_post_delete_handler(sender, instance, **kwargs):
#     Event_instructions.objects.filter(event=instance.event, params=instance.operation.name).delete()
