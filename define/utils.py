# 导入待生成脚本的文件头部设置
from .files_head_setting import models_file_head, admins_file_head, forms_file_head, modelform_footer, views_file_head, urls_file_head, index_html_file_head
from .models import BaseModel, BaseForm, DicList, OperandView, SourceCode
from time import time
import json


# 生成视图查询副本, 被define.admin调用
def copy_form(modeladmin, request, queryset):
    for obj in queryset:
        t = int(time())
        f = BaseForm.objects.create(
            name=f'{obj.name}_query_{t}',
            label=f'{obj.label}_查询视图_{t}',
            basemodel=obj.basemodel,
            is_inquiry=True,
            style=obj.style,
        )

        # 重构meta_data
        meta_data = json.loads(obj.meta_data)
        print('重构meta_data', type(meta_data), meta_data)
        meta_data['name'] = f.name
        meta_data['label'] = f.label
        meta_data['mutate_or_inquiry'] = 'inquiry'
        f.meta_data = json.dumps(meta_data, ensure_ascii=False)
        f.components.add(*obj.components.all())
        f.save()

copy_form.short_description = '生成查询视图副本'


# 生成作业脚本, 被define.admin调用
def generate_source_code(modeladmin, request, queryset):
    source_code = {}
    source_code['dicts_models'], source_code['dicts_admin'], source_code['dicts_data'] = generate_dicts_code()
    source_code['models'] , source_code['admin'] = generate_models_admin_code()
    source_code['forms'] =  generate_forms_code()
    source_code['views'] , source_code['urls'], source_code['templates'] = generate_views_urls_templates_code()

    # 写入数据库
    s = SourceCode.objects.create(
        name = str(int(time())),
        code = json.dumps(source_code, ensure_ascii=False),
    )
    print(f'写入数据库成功, id: {s.id}')

generate_source_code.short_description = '生成作业脚本'


####################################################################################################################
# Create dictionaries models.py, admin.py
####################################################################################################################
def generate_dicts_code():
    print('生成字典 ...')
    dicts_models_script = '''from django.db import models\n\n'''
    dicts_admin_script = '''from django.contrib import admin
from .models import *\n\n'''
    dicts_data = []

    dicts = DicList.objects.all()
    for dic in dicts:
        if 'icpc' not in dic.name:
            dic_name = dic.name.capitalize()
            # construct model script
            model_head = f'class {dic_name}(models.Model):'
            # construct field script
            model_field = '''
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")'''
            # construct model footer script
            model_footer = f'''
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "{dic.label}"
            verbose_name_plural = "{dic.label}"
            '''
            ds =  f'{model_head}{model_field}{model_footer}\n'

            ads = f'''class {dic_name}Admin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register({dic_name}, {dic_name}Admin)\n\n'''

            # 获取字典数据
            if dic.content:
                dicts_data.append({dic_name: dic.content})

            dicts_models_script = dicts_models_script + ds
            dicts_admin_script = dicts_admin_script + ads

    return dicts_models_script, dicts_admin_script, dicts_data


####################################################################################################################
# Create models.py, admin.py
####################################################################################################################
def generate_models_admin_code():
    print('生成models.py, admin.py ...')
    models_script = ''
    admins_script =  ''
    models = BaseModel.objects.all()
    for obj in models:
        s = CreateModelsScript(obj)
        ms, ads = s.create_scripts()
        # construct models script
        models_script = models_script + ms
        # construct admin script
        admins_script = admins_script + ads
    return models_file_head + models_script, admins_file_head + admins_script


class CreateModelsScript:
    def __init__(self, model):
        self.name = model.name
        self.label = model.label
        self.components = model.components.all()

    def create_scripts(self):
        # construct model script
        model_head = f'class {self.name.capitalize()}(models.Model):'

        model_fields = autocomplete_fields = ''
        for component in self.components:
            # construct fields script
            script = self.__create_model_field_script(component)
            model_fields = model_fields + script
            
            # construct admin autocomplete_fields script
            if component.content_type.__dict__['model'] == 'relatedfield':
                autocomplete_fields = autocomplete_fields + f'"{component.content_object.__dict__["name"]}", '

        model_footer = self.__create_model_footer_script()

        # construct model script
        model_script = f'{model_head}{model_fields}{model_footer}\n\n'
        # construct admin script
        admin_script = self.__create_admin_script(autocomplete_fields)

        return model_script, admin_script

    # generate model field script
    def __create_model_field_script(self, component):
        script = ''
        field = component.content_object.__dict__
        component_type = component.content_type.__dict__['model']
        if component_type == 'characterfield':
            script = self.__create_char_field_script(field)
        elif component_type == 'boolfield':
            script = self.__create_bool_field_script(field)
        elif component_type == 'numberfield':
            script = self.__create_number_field_script(field)
        elif component_type == 'dtfield':
            script = self.__create_datetime_field_script(field)
        elif component_type == 'choicefield':
            script = self.__create_choice_field_script(field)
        elif component_type == 'relatedfield':
            field['foreign_key'] = component.content_object.related_content.name.capitalize()
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

        if field['default']:
            f_default = f'default="{field["default"]}", '
        else:
            f_default = ''

        return f'''
    {field['name']} = models.{f_type}(max_length={field['length']}, {f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成布尔型字段定义脚本
    def __create_bool_field_script(self, field):

        f_required = f_default = ''

        if field['type'] == '1':
            f_required = 'null=True, blank=True, '

        if field['default'] == '1':
            f_default = 'default=True, '
        elif field['default'] == '2':
            f_default = 'default=False, '
        else:
            f_required = 'null=True, blank=True, '            
            
        return f'''
    {field['name']} = models.BooleanField({f_default}{f_required}verbose_name='{field['label']}')'''

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
            f_required = ''
        else:
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
            f_required = ''
        else:
            f_required = 'null=True, blank=True, '

        return f'''
    {field['name']} = models.{f_type}({f_default}{f_required}verbose_name='{field['label']}')'''

    # 生成选择型字段定义脚本
    def __create_choice_field_script(self, field):
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
    def __create_related_field_script(self, field):
        if field['type'] == 'Select':
            f_type = 'Select'
        elif field['type'] == 'RadioSelect':
            f_type = 'RadioSelect'
        elif field['type'] == 'CheckboxSelectMultiple':
            f_type = 'CheckboxSelectMultiple'
        else:
            f_type = 'SelectMultiple'
        
        return f'''
    {field['name']} = models.ForeignKey({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', on_delete=models.CASCADE, verbose_name='{field['label']}')'''

    # generate model footer script
    def __create_model_footer_script(self):
        return f'''
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '{self.label}'
        verbose_name_plural = '{self.label}'

    def get_absolute_url(self):
        return reverse('{self.name}_detail_url', kwargs={{'slug': self.slug}})

    def get_update_url(self):
        return reverse('{self.name}_update_url', kwargs={{'slug': self.slug}})

    def get_delete_url(self):
        return reverse('{self.name}_delete_url', kwargs={{'slug': self.slug}})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{{int(time())}}'
        super().save(*args, **kwargs)        
        '''

    # generate admin script
    def __create_admin_script(self, autocomplete_fields):
        c_model_name = self.name.capitalize()
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
        return admin_script


####################################################################################################################
# generate forms.py script
####################################################################################################################
def generate_forms_code():
    print('生成forms.py ...')
    forms_script = ''
    forms = BaseForm.objects.all()
    for form in forms:
        s = CreateFormsScript(form)
        fs = s.create_scripts()
        forms_script = forms_script + fs
    return forms_file_head + forms_script


class CreateFormsScript:
    def __init__(self, form):
        self.name = form.name.capitalize()
        self.label = form.label
        self.model = form.basemodel.name.capitalize()
        self.style = form.style
        self.components = form.components.all()
        self.fields = ''
        self.widgets = ''

    def create_scripts(self):
        for component in self.components:
            field_name = component.content_object.__dict__['name']
            # get fields
            self.fields = self.fields + f'\'{field_name}\', '

            # get widgets
            if component.content_type.__dict__['model'] in ['choicefield', 'relatedfield']:
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

        # construct forms script
        modelform_head = f'''
class {self.name}_ModelForm(ModelForm):'''

        modelform_body = f'''
    class Meta:
        model = {self.model}
        fields = [{self.fields}]
        {self.widgets}
        '''

        return f'{modelform_head}{modelform_body}{modelform_footer}'


####################################################################################################################
# generate views.py, urls.py, templates.html, templates\index.html script
####################################################################################################################
def generate_views_urls_templates_code():
    print('生成views.py, urls.py, templates.html, index.html ...')
    views_script = ''
    urls_script = ''
    index_html_script = ''
    templates_code = []

    views = OperandView.objects.all()
    for obj in views:

        ################################################################################
        # Insert into core.models.Form (Auto generate corresponding operation)
        ################################################################################

        # create views.py, template.html, urls.py
        # inquire_forms = [(f['name'], f['style'], f['label']) for f in list(obj.inquire_forms.all().values())]
        # mutate_forms = [(f['name'], f['style'], f['label']) for f in list(obj.mutate_forms.all().values())]

        # s = CreateViewsScript(obj.name, obj.label, obj.axis_field, inquire_forms, mutate_forms)
        s = CreateViewsScript(obj)
        vs, hs, us, ihs = s.create_script()
        
        # construct views script
        views_script = views_script + vs
        # construct urls script
        urls_script = urls_script + us
        # create templates.html
        templates_code.append({f'{obj.name}_edit.html': hs})
        # construct index.html script
        index_html_script = index_html_script + ihs

    # generate views script
    views_code = views_file_head + views_script
    # generate urls script
    urls_code = urls_file_head + urls_script + '\n]'
    # generate index.html script, append to templates
    index_html_code = index_html_file_head + index_html_script + '\n</section>\n{% endblock %}'
    templates_code.append({'index.html': index_html_code})

    return views_code, urls_code, templates_code


# generate views.py, urls.py, templates.html, index.html script
class CreateViewsScript:
    # def __init__(self, operand_name, operand_label, axis_field, inquire_forms, mutate_forms):
    def __init__(self, obj):
        self.operand_name = obj.name
        self.operand_label = obj.label
        self.managed_entity = obj.managed_entity
        forms = json.loads(obj.forms.meta_data)
        self.inquire_forms, self.mutate_forms = self.__get_forms_list(forms)

        self.view_name = self.operand_name.capitalize() + '_CreateView'
        self.template_name = self.operand_name + '_edit.html'
        self.success_url = '/'
        self.form_class = self.mutate_forms[0][0].capitalize() + '_ModelForm'

        self.url = self.operand_name + '_create_url'


    def __get_forms_list(self, forms):
        inquire_forms = []
        mutate_forms = []
        for form in forms:
            if form['mutate_or_inquiry'] == 'inquiry':
                inquire_forms.append((form['name'], form['style'], form['label']))
            else:
                mutate_forms.append((form['name'], form['style'], form['label']))
        return inquire_forms, mutate_forms

    # create views.py, template.html, urls.py, index.html script
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


    # 迭代forms列表获得各部分构造参数
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


    # 构造views脚本
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

    # 构造html脚本
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

    
    # 构造urls脚本
    def __construct_url_script(self):
        return f'''
    path('{self.operand_name}', {self.view_name}.as_view(), name='{self.url}'),'''


    # 构造index.html脚本
    def __construct_index_html_script(self):
        return f'''<a class='list-group-item' href='{{% url "{self.url}" %}}'>
		{self.operand_label}
	</a>
        '''