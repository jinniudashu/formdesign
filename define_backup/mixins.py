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
        head_script = f'class {self.name.capitalize()}(HsscBuessinessFormBase):'
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
            admin_script = f'''
admin.site.register({name})
'''
        else:
            admin_script = f'''
@admin.register({name})
class {name}Admin(admin.ModelAdmin):
    autocomplete_fields = [{autocomplete_fields}]
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


class GenerateViewsScriptMixin:
    # 生成运行时脚本的views, urls, templates
    def generate_script(self):
        create_view_name = self.name.capitalize() + '_CreateView'
        update_view_name = self.name.capitalize() + '_UpdateView'
        # self.edit_template_name = f'{self.operand_name}_edit.html'
        # self.success_url = '/'
        script = {}
        script['views'] = self.__construct_view_script(create_view_name, update_view_name)
        script['urls'] = self.__construct_url_script(create_view_name, update_view_name)
        script['templates'] = self.__construct_html_script()

        return script

    # 构造views脚本
    def __construct_view_script(self, create_view_name, update_view_name):
        view_model_name = self.operations.all()[0].buessiness_forms.all()[0].name.capitalize()
        base_model_name = self.managed_entity.base_form.name.capitalize()
        base_form_name = f'{base_model_name}_ModelForm'

        create_script_attribute_forms_post = ''
        create_script_attribute_forms_get = ''
        create_script_attribute_forms_context = ''
        create_script_attribute_forms_valid = ''
        form_index = 0

        for operation in self.operations.all():
            for form in operation.buessiness_forms.all():
                create_script_attribute_forms_post = f'''{create_script_attribute_forms_post}
            attribute_form{form_index} = {form.name.capitalize()}_ModelForm(self.request.POST, prefix="attribute_form{form_index}")'''
                create_script_attribute_forms_get = f'''{create_script_attribute_forms_get}
            attribute_form{form_index} = {form.name.capitalize()}_ModelForm(prefix="attribute_form{form_index}")'''
                create_script_attribute_forms_context = f'''{create_script_attribute_forms_context}
        context['attribute_form{form_index}'] = attribute_form{form_index}'''
                create_script_attribute_forms_valid = f'''{create_script_attribute_forms_valid}
        f = context['attribute_form{form_index}'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()'''
                form_index += 1

        # create view
        create_script_head = f'''
class {create_view_name}(CreateView):
    model = {view_model_name}
    customer = None
    entity_base_info = {base_model_name}.objects.get(customer=customer)
    context = {{}}
'''
        create_script_body = f'''
    def get_context_data(self, **kwargs):
        context = super({create_view_name}, self).get_context_data(**kwargs)
        base_form = {base_form_name}(instance=self.entity_base_info, prefix="base_form")
        if self.request.method == 'POST':{create_script_attribute_forms_post}
        else:{create_script_attribute_forms_get}
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

#         # update view
#         update_script_head = f'''
# class {update_view_name}(CreateView):
#     model = {self.__class__.__name__}
#     operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])

#     if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
#         return redirect(reverse('index'))
#     operation_proc.group.set([])  # 设置作业进程所属角色组为空

#     # 构造作业开始消息参数
#     operand_started.send(sender={self.name}_update, operation_proc=operation_proc, ocode='rtr', operator=request.user)

#     customer = operation_proc.customer
#     basic_personal_information = Basic_personal_information.objects.get(customer=customer)
#     context = {{}}
#         '''

#         update_script_body = f'''
#         if request.method == 'POST':
#                 # 构造作业完成消息参数
#                 operand_finished.send(sender={self.name}_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
#                 return redirect(reverse('index'))
#         else:
#             pass
#         # context'''

#         update_script_foot = f'''
#         context['proc_id'] = kwargs['id']
#         return render(request, '{self.name}_update.html', context)

#         '''

#         return f'{create_script_head}{create_script_body}\n\n{update_script_head}{update_script_body}{update_script_foot}'
        return f'{create_script_head}{create_script_body}'

    # 构造html脚本
    def __construct_html_script(self):
        _hs = f'''
                    <h5>{self.name}</h5>
                    {{{{ {self.name}.as_p }}}}
                    <hr>'''            
        script_head = f'''{{% extends "base.html" %}}

    {{% load crispy_forms_tags %}}

    {{% block content %}}
    '''

        create_script_body = f'''
        <form action={{% url '{self.name}_create_url' %}} method='POST' enctype='multipart/form-data'> 
            {{% csrf_token %}}
                ''' + _hs

        update_script_body = f'''
        <form action={{% url '{self.name}_update_url' proc_id %}} method='POST' enctype='multipart/form-data'> 
            {{% csrf_token %}}
                ''' + _hs

        script_foot = f'''
            <input type="submit" value="提交" /> 
        </form>

    {{% endblock %}}
    '''

        s_create = f'{script_head}{create_script_body}{script_foot}'
        s_update = f'{script_head}{update_script_body}{script_foot}'
        return [{f'{self.name}_create.html': s_create}, {f'{self.name}_update.html': s_update}]

        # 构造urls脚本
    def __construct_url_script(self, create_view_name, update_view_name):
        return f'''
    path('{self.name}/create', {create_view_name}.as_view(), name='{self.name}_create_url'),'''
    # path('{self.name}/<int:id>/update', {update_view_name}.as_view(), name='{self.name}_update_url'),'''

