class GenerateModelsScriptMixin:
    # 生成models, admin, forms脚本
    def generate_script(self):
        script = {}
        script['models'], script['admin'] = self.__create_model_script()
        script['forms'] = self.__create_form_script()
        return script

    # generate model and admin script
    def __create_model_script(self):
        # construct model script
        head_script = f'class {self.name.capitalize()}(HsscFormModel):'
        fields_script = autocomplete_fields = ''

        # !!!待修改：compontents = form.components.all() + form.component_groups.all()
        for component in self.components.all():
            # construct fields script
            _script = self.__create_model_field_script(component)
            fields_script = fields_script + _script
            # construct admin autocomplete_fields script
            if component.content_object.__class__.__name__ == 'RelatedField':
                autocomplete_fields = autocomplete_fields + f'"{component.content_object.name}", '

        footer_script = self.__create_model_footer_script()

        # construct model and admin script
        model_script = f'{head_script}{fields_script}{footer_script}\n\n'
        admin_script = self.__create_admin_script(autocomplete_fields)
        return model_script, admin_script

    # generate admin script
    def __create_admin_script(self, autocomplete_fields):
        name = self.name.capitalize()
        if autocomplete_fields == '':
            _body = f'pass'
        else:
            _body = f'autocomplete_fields = [{autocomplete_fields}]'

        admin_script = f'''
class {name}Admin(HsscFormAdmin):
    {_body}
admin.site.register({name}, {name}Admin)
clinic_site.register({name}, {name}Admin)
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

    def __create_form_script(self):
        fields = ''
        widgets = ''

        for component in self.components.all():
            field_name = component.content_object.name
            # get fields
            if field_name:
                fields = f'{fields}\'{field_name}\', '
            # get widgets
            if component.content_type.__dict__['model']=='relatedfield':
                field_type = component.content_object.type
                if field_type == 'Select':
                    type = 'Select'
                elif field_type == 'RadioSelect':
                    type = 'RadioSelect'
                elif field_type == 'CheckboxSelectMultiple':
                    type = 'CheckboxSelectMultiple'
                else:
                    type = 'SelectMultiple'
                widgets = f'{widgets}\'{field_name}\': {type}, '
        if widgets != '':
            widgets = f'widgets = {{{widgets}}}'

        # construct form script
        return f'''
class {self.name.capitalize()}_ModelForm(ModelForm):
    class Meta:
        model = {self.name.capitalize()}
        fields = [{fields}]
        {widgets}
    '''


class GenerateServiceScriptMixin:
    # 生成运行时脚本的models, admin, views, urls, templates
    def generate_script(self):
        create_view_name = self.name.capitalize() + '_CreateView'
        update_view_name = self.name.capitalize() + '_UpdateView'
        # edit_template_name = f'{self.name}_edit.html'
        script = {}
        script['views'] = self.__construct_view_script(create_view_name, update_view_name)
        script['urls'] = self.__construct_url_script(create_view_name, update_view_name)
        script['templates'] = self.__construct_html_script()

        script['models'], script['admin'] = self.__create_model_script()

        return script
    
    # 构造views脚本
    def __construct_view_script(self, create_view_name, update_view_name):
        view_model_name = self.buessiness_forms.all()[0].name.capitalize()
        base_model_name = self.managed_entity.base_form.name.capitalize()
        base_form_name = f'{base_model_name}_ModelForm'

        create_script_attribute_forms_post = ''
        create_script_attribute_forms_get = ''
        update_script_attribute_forms_get = ''
        create_script_attribute_forms_context = ''
        create_script_attribute_forms_valid = ''

        for form in self.buessiness_forms.all():
            create_script_attribute_forms_post = f'''{create_script_attribute_forms_post}
            {form.name.lower()}_form = {form.name.capitalize()}_ModelForm(self.request.POST, prefix="{form.name.lower()}_form")'''
            create_script_attribute_forms_get = f'''{create_script_attribute_forms_get}
            {form.name.lower()}_form = {form.name.capitalize()}_ModelForm(prefix="{form.name.lower()}_form")'''
            update_script_attribute_forms_get = f'''{update_script_attribute_forms_get}
            {form.name.lower()}_form = {form.name.capitalize()}_ModelForm(instance={form.name.capitalize()}.objects.get(pid=kwargs['id']), prefix="{form.name.lower()}_form")'''
            create_script_attribute_forms_context = f'''{create_script_attribute_forms_context}
        context['{form.name.lower()}_form'] = {form.name.lower()}_form'''
            create_script_attribute_forms_valid = f'''{create_script_attribute_forms_valid}
        f = context['{form.name.lower()}_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()'''

        # create view
        create_script_head = f'''
class {create_view_name}(CreateView):
    success_url = 'forms/'
    template_name = '{self.name}_create.html'
    form_class = {view_model_name}_ModelForm  # the first form ModelForm class
    model = {view_model_name}
    context = {{}}
'''
        create_script_body = f'''
    def get_context_data(self, **kwargs):
        context = super({create_view_name}, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = {base_form_name}(self.request.POST, prefix="base_form"){create_script_attribute_forms_post}
        else:
            base_form = {base_form_name}(prefix="base_form"){create_script_attribute_forms_get}
        # context
        context['base_form'] = base_form{create_script_attribute_forms_context}
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid{create_script_attribute_forms_valid}
        return super({create_view_name}, self).form_valid(form)
'''

        # update view
        update_script_head = f'''
class {update_view_name}(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = '{self.name}_update.html'
    form_class = {view_model_name}_ModelForm # the first form ModelForm class
    model = {view_model_name}

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {{}}
        '''

        update_script_body = f'''
    def get_context_data(self, **kwargs):
        context = super({update_view_name}, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = {base_form_name}(instance={base_model_name}.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':{create_script_attribute_forms_post}
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:{update_script_attribute_forms_get}
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form{create_script_attribute_forms_context}
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid{create_script_attribute_forms_valid}
        return super({create_view_name}, self).form_valid(form)
'''

        return f'{create_script_head}{create_script_body}\n\n{update_script_head}{update_script_body}'

    # 构造html脚本
    def __construct_html_script(self):
        _hs = f'''
        <form action='' method='GET' enctype='multipart/form-data'> 
            {{% csrf_token %}}                
            <h5>{self.managed_entity.base_form.label}</h5>
            {{{{ base_form.as_table }}}}
        </form>
        <hr>'''
        create_hs = f'''<form action={{% url '{self.name}_create_url' %}} method='POST' enctype='multipart/form-data'> '''
        update_hs = f'''<form action={{% url '{self.name}_update_url' id %}} method='POST' enctype='multipart/form-data'> '''
        for form in self.buessiness_forms.all():
            create_hs = f'''{create_hs}
            {{% csrf_token %}}                
            <h5>{form.label}</h5>
            {{{{ {form.name.lower()}_form.as_p }}}}
        <hr>'''
            update_hs = f'''{update_hs}
            {{% csrf_token %}}                
            <h5>{form.label}</h5>
            {{{{ {form.name.lower()}_form.as_p }}}}
        <hr>'''

        script_head = f'''{{% extends "base.html" %}}
    {{% block content %}}
    '''

        create_script_body = _hs + create_hs

        update_script_body = _hs + update_hs

        script_foot = f'''
        </form>
        <input type="submit" value="完成服务" onclick="formSave('{form.name.lower()}_form')" />
    {{% endblock %}}
    '''

        s_create = f'{script_head}{create_script_body}{script_foot}'
        s_update = f'{script_head}{update_script_body}{script_foot}'
        return [{f'{self.name}_create.html': s_create}, {f'{self.name}_update.html': s_update}]

    # 构造urls脚本
    def __construct_url_script(self, create_view_name, update_view_name):
        return f'''
    path('{self.name}/create', {create_view_name}.as_view(), name='{self.name}_create_url'),
    path('{self.name}/<int:id>/update', {update_view_name}.as_view(), name='{self.name}_update_url'),'''

# ***************************************************************************
# ***************************************************************************

    # generate model and admin script
    def __create_model_script(self):
        # construct model script
        head_script = f'class {self.name.capitalize()}(HsscFormModel):'

        # 添加表头字段
        fields_script, header_fields = self.__construct_header_fields_script()

        # admin.py脚本设置
        fieldssets = f'("基本信息", {{"fields": (({header_fields}),)}}), '
        autocomplete_fields = ''

        for form in self.buessiness_forms.all():
        # !!!待修改：compontents = form.components.all() + form.component_groups.all()
            form_fields = ''
            for component in form.components.all():
                # construct fields script
                _script = self.__create_model_field_script(component)
                fields_script = fields_script + _script
                # construct admin body fields script
                form_fields = form_fields + f'"{component.content_object.name}", '
                if component.content_object.__class__.__name__ == 'RelatedField':
                    autocomplete_fields = autocomplete_fields + f'"{component.content_object.name}", '
            # construct admin fieldset script
            fieldssets_set = f'\n        ("{form.label}", {{"fields": ({form_fields})}}), '
            fieldssets = fieldssets + fieldssets_set
        # construct admin script
        admin_script = self.__create_admin_script(fieldssets, autocomplete_fields, header_fields)

        # construct model script
        footer_script = self.__create_model_footer_script()
        model_script = f'{head_script}{fields_script}{footer_script}\n\n'

        return model_script, admin_script

    # generate admin script
    def __create_admin_script(self, fieldssets, autocomplete_fields, readonly_fields):
        name = self.name.capitalize()
        fieldssets = f'fieldsets = ({fieldssets})'
        readonly_fields = f'readonly_fields = [{readonly_fields}]'
        if autocomplete_fields:
            autocomplete_fields = f'autocomplete_fields = [{autocomplete_fields}]'

        admin_script = f'''
class {name}Admin(HsscFormAdmin):
    {fieldssets}
    {autocomplete_fields}
    {readonly_fields}
admin.site.register({name}, {name}Admin)
clinic_site.register({name}, {name}Admin)
'''
        return admin_script

    # 构建表头字段脚本
    def __construct_header_fields_script(self):
        fields_script = ''
        header_fields = ''
        for component in self.managed_entity.header_fields.all():
            # construct fields script
            _script = self.__create_model_field_script(component)
            fields_script = fields_script + _script
            header_fields = header_fields + f'"{component.content_object.name}", '
        # 如果服务表单内包含基本信息表，返回空表头字段
        if self.managed_entity.base_form in self.buessiness_forms.all():
            header_fields = ''
        return fields_script, header_fields

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

    # generate model footer script
    def __create_model_footer_script(self):
        return f'''

    class Meta:
        verbose_name = '{self.label}'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        '''
