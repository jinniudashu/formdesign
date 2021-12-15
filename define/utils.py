import os

# 导入待生成脚本的文件头部设置
from .files_head_setting import models_file_head, admins_file_head, forms_file_head, modelform_footer, views_file_head, urls_file_head, index_html_file_head
from .models import BaseModel, BaseForm

# 写入文件
def write_to_file(file_name, content, mode='w'):
    output_path = '.\\forms\\'   # views.py urls.py 导出路径
    with open(f'{output_path}{file_name}', mode, encoding='utf-8') as f:
        f.write(content)
    return      


# 被define.admin调用
def generate_models_forms_scripts():

    # 生成字符型字段定义脚本
    def create_char_field_script(field):
        if field['type'] == 'CharField':
            f_type = 'CharField'
        else:
            f_type = 'TextField'

        if field['required']:
            f_required = ''
        else:
            f_required = 'null=True, blank=True, '

        if field['default']:
            f_default = f'default="{field["default"]}", '
        else:
            f_default = ''

        return f'''
    {field['name']} = models.{f_type}(max_length={field['length']}, {f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成数字型字段定义脚本
    def create_number_field_script(field):
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
            f_required = ''
        else:
            f_required = 'null=True, blank=True, '

        return f'''
    {field['name']} = models.{f_type}({f_dicimal}{f_default}{f_required}verbose_name='{field['label']}')
    {field['name']}_standard_value = models.{f_type}({f_standard_value}{f_required}verbose_name='{field['label']}标准值')
    {field['name']}_up_limit = models.{f_type}({f_up_limit}{f_required}verbose_name='{field['label']}上限')
    {field['name']}_down_limit = models.{f_type}({f_down_limit}{f_required}verbose_name='{field['label']}下限')'''
    
    # 生成日期型字段定义脚本
    def create_datetime_field_script(field):
        f_default = ''
        if field['type'] == 'DateTimeField':
            f_type = 'DateTimeField'
            if field['default_now']: f_default = 'default=timezone.now(), '
        else:
            f_type = 'DateField'
            if field['default_now']: f_default = 'default=date.today(), '
        
        if field['required']:
            f_required = ''
        else:
            f_required = 'null=True, blank=True, '

        return f'''
    {field['name']} = models.{f_type}({f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成选择型字段定义脚本
    def create_choice_field_script(field):
        if field['type'] == 'Select':
            f_type = 'Select'
        elif field['type'] == 'RadioSelect':
            f_type = 'RadioSelect'
        elif field['type'] == 'CheckboxSelectMultiple':
            f_type = 'CheckboxSelectMultiple'
        else:
            f_type = 'SelectMultiple'

        f_enum = f'{field["name"].capitalize()}Enum'
        f_choices = ''
        for index, name in enumerate(field['options'].split('\r\n')):
            f_choices=f_choices + (f'({index}, "{name}"),')

        if field['default_first']:
            f_default = 'default=0, '
        else:
            f_default = ''

        if field['required']:
            f_required = ''
        else:
            f_required = 'null=True, blank=True, '

        return f'''
    {f_enum} = [{f_choices}]
    {field['name']} = models.PositiveSmallIntegerField({f_default}{f_required}choices={f_enum}, verbose_name='{field['label']}')'''

    # 生成外键字段定义脚本
    def create_related_field_script(field):
        if field['type'] == 'Select':
            f_type = 'Select'
        elif field['type'] == 'RadioSelect':
            f_type = 'RadioSelect'
        elif field['type'] == 'CheckboxSelectMultiple':
            f_type = 'CheckboxSelectMultiple'
        else:
            f_type = 'SelectMultiple'
        
        return f'''
    {field['name']} = models.ForeignKey({field['foreign_key'].capitalize()}, on_delete=models.CASCADE, verbose_name='{field['label']}')'''

    # generate model field script
    def create_model_field_script(component):
        field = component.content_object.__dict__
        component_type = component.content_type.__dict__['model']
        if component_type == 'characterfield':
            script = create_char_field_script(field)
        elif component_type == 'numberfield':
            script = create_number_field_script(field)
        elif component_type == 'dtfield':
            script = create_datetime_field_script(field)
        elif component_type == 'choicefield':
            script = create_choice_field_script(field)
        elif component_type == 'relatedfield':
            field['foreign_key'] = component.content_object.related_content.model
            script = create_related_field_script(field)
        return script

    ####################################################################################################################
    # construct models and admin script
    ####################################################################################################################
    models_script = admins_script =  ''
    models = BaseModel.objects.all()
    for obj in models:
        model_name = obj.name
        model_label = obj.label

        # construct models script
        model_head = f'class {model_name.capitalize()}(models.Model):'

        model_fields = autocomplete_fields = ''
        for component in obj.components.all():
            # construct fields script
            script = create_model_field_script(component)
            model_fields = model_fields + script
            
            # construct admin autocomplete_fields script
            if component.content_type.__dict__['model'] == 'relatedfield':
                autocomplete_fields = autocomplete_fields + f'"{component.content_object.__dict__["name"]}", '

        model_body = f'''

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '{model_label}'
        verbose_name_plural = '{model_label}'

    def get_absolute_url(self):
        return reverse('{model_name}_detail_url', kwargs={{'slug': self.slug}})

    def get_update_url(self):
        return reverse('{model_name}_update_url', kwargs={{'slug': self.slug}})

    def get_delete_url(self):
        return reverse('{model_name}_delete_url', kwargs={{'slug': self.slug}})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{{int(time())}}'
        super().save(*args, **kwargs)        
        '''
        model_script = f'{model_head}{model_fields}{model_body}\n\n'
        models_script = models_script + model_script

        # construct admin script
        c_model_name = model_name.capitalize()
        if autocomplete_fields != '':
            admin_script = f'''
class {c_model_name}Admin(admin.ModelAdmin):
    autocomplete_fields = [{autocomplete_fields}]
admin.site.register({c_model_name}, {c_model_name}Admin)
'''
        else:
            admin_script = f'''
admin.site.register({c_model_name})
'''
        
        admins_script = admins_script + admin_script

    # add header to models.py
    models_script = models_file_head + models_script
    write_to_file('models.py', models_script)

    # generate admin script
    admins_script = admins_file_head + admins_script
    write_to_file('admin.py', admins_script)


    ####################################################################################################################
    # generate forms.py script
    ####################################################################################################################
    forms_script = ''
    forms = BaseForm.objects.all()
    for form in forms:
        f_name = form.name.capitalize()
        form_label = form.label
        f_model = form.basemodel.name.capitalize()
        form_style = form.style
        f_fields = f_widgets = ''
        for component in form.components.all():
            field_name = component.content_object.__dict__['name']
            # get fields
            f_fields = f_fields + f'\'{field_name}\', '

            # get widgets
            if component.content_type.__dict__['model'] in ['choicefield', 'relatedfield']:
                field_type = component.content_object.__dict__['type']
                if field_type == 'Select':
                    f_type = 'Select'
                elif field_type == 'RadioSelect':
                    f_type = 'RadioSelect'
                elif field_type == 'CheckboxSelectMultiple':
                    f_type = 'CheckboxSelectMultiple'
                else:
                    f_type = 'SelectMultiple'
                f_widgets = f_widgets + f'\'{field_name}\': {f_type}, '

        if f_widgets != '':
            f_widgets = f'widgets = {{{f_widgets}}}'

        # construct forms script
        modelform_head = f'''
class {f_name}_ModelForm(ModelForm):'''

        modelform_body = f'''
    class Meta:
        model = {f_model}
        fields = [{f_fields}]
        {f_widgets}
        '''

        modelform_script = f'{modelform_head}{modelform_body}{modelform_footer}'
        forms_script = forms_script + modelform_script
    
    # construct forms.py script
    forms_script =  forms_file_head + forms_script
    write_to_file('forms.py', forms_script)



# 被define.admin调用
def generate_views_urls_templates_scripts(modeladmin, request, queryset):

    ####################################################################################################################
    # Create models.py, admin.py, forms.py
    ####################################################################################################################
    print('生成models.py, admin.py, forms.py ...')
    generate_models_forms_scripts()

    print('生成views.py, urls.py, templates.html, index.html ...')
    views_script = urls_script = index_html_script = ''
    for obj in queryset:
        ################################################################################
        # Insert into core.models.Form (Auto generate corresponding operation)
        ################################################################################

        # create views.py, template.html, urls.py
        inquire_forms = [(f['name'], f['style'], f['label']) for f in list(obj.inquire_forms.all().values())]
        mutate_forms = [(f['name'], f['style'], f['label']) for f in list(obj.mutate_forms.all().values())]

        s = CreateViewsScripts(obj.name, obj.label, obj.axis_field, inquire_forms, mutate_forms)
        vs, hs, us, ihs = s.create_script()

        # construct views script
        views_script = views_script + vs
        # construct urls script
        urls_script = urls_script + us
        # create template.html
        write_to_file(f'templates\\{obj.name}_edit.html', hs)
        # construct index.html script
        index_html_script = index_html_script + ihs

    # add header to views.py
    views_script = views_file_head + views_script
    # add header to urls.py
    urls_script = urls_file_head + urls_script + '\n]'
    # add header to index.html
    index_html_script = index_html_file_head + index_html_script + '\n</section>\n{% endblock %}'

    # 写入views.py
    write_to_file('views.py', views_script)
    # 写入urls.py
    write_to_file('urls.py', urls_script)
    # 写入index.html
    write_to_file('templates\\index.html', index_html_script)

    ################################################################################
    # 写入作业库
    ################################################################################

generate_views_urls_templates_scripts.short_description = '生成作业视图脚本'



class CreateViewsScripts:

    def __init__(self, operand_name, operand_label, axis_field, inquire_forms, mutate_forms):
        self.operand_name = operand_name
        self.operand_label = operand_label
        self.axis_field = axis_field
        self.inquire_forms = inquire_forms
        self.mutate_forms = mutate_forms

        self.view_name = operand_name.capitalize() + '_CreateView'
        self.template_name = operand_name + '_edit.html'
        self.success_url = '/'
        self.form_class = mutate_forms[0][0].capitalize() + '_ModelForm'

        self.url = self.operand_name + '_create_url'

    def create_script(self):

        # 迭代获得各部分构造参数
        vs, hs = self.__iterate_forms()

        # views.py
        view_script = self.__construct_view_script(vs)

        # .html
        html_script = self.__construct_html_script(hs)

        # urls.py
        url_script = self.__construct_url_script()
        
        # index.html
        index_html_script = self.__construct_index_html_script()

        return view_script, html_script, url_script, index_html_script


    def __iterate_forms(self):
        i = 0       # count forms

        # 把view分为6个部分
        s0 = ''     # inquire_forms
        s1 = ''     # mutate_formsets
        s2 = ''     # POST mutate_forms
        s3 = ''     # GET mutate_forms
        s4 = ''     # context
        s5 = ''     # form_valid

        s6 = ''     # template scripts

        # Iterate inquire_forms
        for form in self.inquire_forms:
            s = c = h = ''
            if form[1] == 'detail':
                s = f'''
        form{i} = {form[0].capitalize()}_ModelForm(instance=self.customer, prefix="form{i}")'''
                c = f'''
        context['form{i}'] = form{i}'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ form{i}.as_p }}}}
        <hr>'''

            else:
                s = f'''
        Formset{i} = modelformset_factory({form[0].capitalize()}, form={form[0].capitalize()}_ModelForm, extra=2)
        # formset{i} = Formset{i}(queryset=self.customer.{form[0].lower()}.all(), prefix="formset{i}")
        formset{i} = Formset{i}(prefix="formset{i}")'''
                c = f'''
        context['formset{i}'] = formset{i}'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ formset{i}.as_p }}}}
        <hr>'''

            s0 = s0 + s
            s4 = s4 + c
            s6 = s6 + h
            i += 1
        
        # Iterate mutate_formsets
        for form in self.mutate_forms:
            s_1=s_2=s_3=c=s_5= h =''

            if form[1] == 'detail':
                s_2 = f'''
            form{i} = {form[0].capitalize()}_ModelForm(self.request.POST, prefix="form{i}")'''
                s_3 = f'''
            form{i} = {form[0].capitalize()}_ModelForm(prefix="form{i}")'''
                c = f'''
        context['form{i}'] = form{i}'''
                s_5 = f'''
        f = context['form{i}'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                '''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ form{i}.as_p }}}}
        <hr>'''

            else:
                s_1 = f'''
        Formset{i} = modelformset_factory({form[0].capitalize()}, form={form[0].capitalize()}_ModelForm, extra=2)'''
                s_2 = f'''
            formset{i} = Formset{i}(self.request.POST, prefix="formset{i}")'''
                s_3 = f'''
            formset{i} = Formset{i}(prefix="formset{i}")'''
                c = f'''
        context['formset{i}'] = formset{i}'''
                s_5 = f'''
        for form in context['formset{i}']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                '''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ formset{i}.as_p }}}}
        <hr>'''

            s1 = s1 + s_1
            s2 = s2 + s_2
            s3 = s3 + s_3
            s4 = s4 + c
            s5 = s5 + s_5

            s6 = s6 + h

            i += 1

        vs = [s0, s1, s2, s3, s4, s5]
        
        return vs, s6


    def __construct_view_script(self, vs):

        script_head = f'''
class {self.view_name}(CreateView):
    template_name = '{self.template_name}'
    success_url = '{self.success_url}'
    form_class = {self.form_class}

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super({self.view_name}, self).get_context_data(**kwargs)
        '''

        script_body = f'''
        # inquire_forms''' + vs[0] + f'''
        # mutate_formsets''' + vs[1] + f'''
        # mutate_forms
        if self.request.method == 'POST':'''+ vs[2] + f'''
        else:''' + vs[3] + f'''
        # context''' + vs[4] + f'''

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid''' + vs[5]
        
        script_foot = f'''
        return super({self.view_name}, self).form_valid(form)

        '''

        s = f'{script_head}{script_body}{script_foot}'
        return s

    def __construct_html_script(self, hs):
        script_head = f'''{{% extends "base.html" %}}

{{% load crispy_forms_tags %}}

{{% block content %}}
'''

        script_body = f'''
	<form action={{% url '{self.url}' %}} method='POST' enctype='multipart/form-data'> 
		{{% csrf_token %}}
            ''' + hs

        script_foot = f'''
		<input type="submit" value="提交" /> 
	</form>

{{% endblock %}}
'''

        s = f'{script_head}{script_body}{script_foot}'
        return s

    
    def __construct_url_script(self):
        return f'''
    path('{self.operand_name}', {self.view_name}.as_view(), name='{self.url}'),'''


    def __construct_index_html_script(self):
        return f'''<a class='list-group-item' href='{{% url "{self.url}" %}}'>
		{self.operand_label}
	</a>
        '''
