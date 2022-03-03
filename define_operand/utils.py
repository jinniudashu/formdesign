# 导入待生成脚本的文件头部设置
from define_dict.models import DicList
from define_form.models import BaseModel, BaseForm
from define_operand.models import Operation, SourceCode
from define_operand.files_head_setting import models_file_head, admins_file_head, forms_file_head, modelform_footer, views_file_head, urls_file_head, index_html_file_head
from time import time
import json


# 生成作业脚本, 被define_operand.admin调用
def generate_source_code(modeladmin, request, queryset):
    source_code = {}
    source_code['dicts_models'], source_code['dicts_admin'], source_code['dicts_data'] = generate_dicts_code()
    source_code['models'] , source_code['admin'] = generate_models_admin_code()
    source_code['forms'] =  generate_forms_code()
    source_code['views'] , source_code['urls'], source_code['templates'], source_code['operand_views'] = generate_views_urls_templates_code()

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

            # 获取字典数据content???
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

    # 生成布尔型字段定义脚本
    def __create_bool_field_script(self, field):

        f_required = f_default = ''

        if field['type'] == '1':
            f_required = 'null=True, blank=True, '
        else:
            f_required = 'null=True, '

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
            f_required = 'null=True, '
        else:
            f_required = 'null=True, blank=True, '

        return f'''
    {f_enum} = [{f_choices}]
    {field['name']} = models.PositiveSmallIntegerField({f_default}{f_required}choices={f_enum}, verbose_name='{field['label']}')'''

    # 生成外键字段定义脚本
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
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

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
    operand_views = []

    views = Operation.objects.filter(forms__isnull=False)
    for obj in views:
        # construct core.models.Operation
        operand_view = {
            'name': obj.name,
            'label': obj.label,
            'forms': obj.forms.meta_data,
        }
        operand_views.append(operand_view)

        # create views.py, template.html, urls.py
        s = CreateViewsScript(obj)
        vs, us, chs, uhs, ihs = s.create_script()
        
        # construct views script
        views_script = views_script + vs
        # construct urls script
        urls_script = urls_script + us
        # create templates.html
        templates_code.append({f'{obj.name}_create.html': chs})
        templates_code.append({f'{obj.name}_update.html': uhs})
        # construct index.html script
        index_html_script = index_html_script + ihs

    # generate views script
    views_code = views_file_head + views_script
    # generate urls script
    urls_code = urls_file_head + urls_script + '\n]'
    # generate index.html script, append to templates
    index_html_code = index_html_file_head + index_html_script + '\n</section>\n{% endblock %}'
    templates_code.append({'index.html': index_html_code})

    return views_code, urls_code, templates_code, operand_views


# generate views.py, urls.py, templates.html, index.html script
class CreateViewsScript:
    def __init__(self, obj):
        self.operand_name = obj.name
        self.operand_label = obj.label
        self.managed_entity = obj.forms.managed_entity
        forms = json.loads(obj.forms.meta_data)
        self.inquire_forms, self.mutate_forms = self.__get_forms_list(forms)

        self.view_name = self.operand_name.capitalize() + '_CreateView'
        self.template_name = self.operand_name + '_edit.html'
        self.success_url = '/'
        # 如果作业不包含可修改表单，self.mutate_forms=[]，会报错IndexError: list index out of range
        self.form_class = self.mutate_forms[0][0].capitalize() + '_ModelForm'

        self.url = self.operand_name + '_update_url'

    def __get_forms_list(self, forms):
        inquire_forms = []
        mutate_forms = []
        print('operand_name', self.operand_name)
        print('forms:', forms)
        for form in forms:
            print('form:', form)
            print("form['mutate_or_inquiry']:", form['mutate_or_inquiry'])
            if form['mutate_or_inquiry'] == 'inquiry':
                inquire_forms.append((form['name'], form['style'], form['label'], form['basemodel']))
            else:
                mutate_forms.append((form['name'], form['style'], form['label'], form['basemodel']))
        return inquire_forms, mutate_forms

    # create views.py, template.html, urls.py, index.html script
    def create_script(self):

        # 迭代获得各部分构造参数
        vs, hs = self.__iterate_forms()
        # views.py
        view_script = self.__construct_view_script(vs)
        # .html
        create_html_script, update_html_script = self.__construct_html_script(hs)
        # urls.py
        url_script = self.__construct_url_script()
        # index.html
        index_html_script = self.__construct_index_html_script()

        return view_script, url_script, create_html_script, update_html_script, index_html_script

    # 迭代forms列表获得各部分构造参数(视图函数版本)
    def __iterate_forms(self):
        i = 0       # count forms

        # 把view分为10个部分
        s0 = ''     # inquire_forms
        s1 = ''     # mutate_formsets
        s2 = ''     # POST mutate_forms
        s3 = ''     # GET mutate_forms
        s4 = ''     # context
        s5_if = []  # form_valid if
        s5 = ''     # form_valid save
        s6 = ''     # template scripts
        s7 = ''     # 获取表单实例
        s2_create = s3_create = ''

        # Iterate inquire_forms
        for form in self.inquire_forms:
            s = c = h = ''
            # s = c = h = p = ''
            
    #         p = f'''
    # {form[3]} = {form[3].capitalize()}.objects.get(pid=operation_proc)'''

            if form[1] == 'detail':
                s = f'''
    form_{form[3]} = {form[0].capitalize()}_ModelForm(instance={form[3]}, prefix="{form[3]}")'''
                c = f'''
    context['form_{form[3]}'] = form_{form[3]}'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ form_{form[3]}.as_p }}}}
        <hr>'''

            else:
                s = f'''
    {form[3].capitalize()}_set = modelformset_factory({form[0].capitalize()}, form={form[0].capitalize()}_ModelForm, extra=2)
    # {form[3]}_set = {form[3].capitalize()}_set(queryset={form[3]}_set.{form[0].lower()}.all(), prefix="{form[3]}_set")
    {form[3]}_set = {form[3].capitalize()}_set(prefix="{form[3]}_set")'''
                c = f'''
    context['{form[3]}_set'] = {form[3]}_set'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ {form[3]}_set.as_p }}}}
        <hr>'''

            s0 = s0 + s
            s4 = s4 + c
            s6 = s6 + h
            # s7 = s7 + p

            i += 1
        
        # Iterate mutate_formsets
        for form in self.mutate_forms:
            s_1=s_2=s_3=c=s_5=s_5_if=h=p=''
            s_2_c=s_3_c = ''

            p = f'''
    {form[3]} = {form[3].capitalize()}.objects.get(pid=operation_proc)'''

            if form[1] == 'detail':
                s_2 = f'''
        form_{form[3]} = {form[0].capitalize()}_ModelForm(instance={form[3]}, data=request.POST, prefix="{form[3]}")'''
                s_3 = f'''
        form_{form[3]} = {form[0].capitalize()}_ModelForm(instance={form[3]}, prefix="{form[3]}")'''
                s_2_c = f'''
        form_{form[3]} = {form[0].capitalize()}_ModelForm(request.POST, prefix="{form[3]}")'''
                s_3_c = f'''
        form_{form[3]} = {form[0].capitalize()}_ModelForm(prefix="{form[3]}")'''
                c = f'''
    context['form_{form[3]}'] = form_{form[3]}'''
                s_5_if = f'''form_{form[3]}.is_valid()'''
                s_5 = f'''
            form_{form[3]}.save()'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ form_{form[3]}.as_p }}}}
        <hr>'''

            else:
                s_1 = f'''
        {form[3].capitalize()}_set = modelformset_factory({form[0].capitalize()}, form={form[0].capitalize()}_ModelForm, extra=2)'''
                s_2 = f'''
            {form[3]}_set = {form[3].capitalize()}_set(instance={form[3]}, data=request.POST, prefix="{form[3]}_set")'''
                s_3 = f'''
            {form[3]}_set = {form[3].capitalize()}_set(instance={form[3]}, prefix="{form[3]}_set")'''
                s_2_c = f'''
            {form[3]}_set = {form[3].capitalize()}_set(request.POST, prefix="{form[3]}_set")'''
                s_3_c = f'''
            {form[3]}_set = {form[3].capitalize()}_set(prefix="{form[3]}_set")'''
                c = f'''
    context['{form[3]}_set'] = {form[3]}_set'''
                s_5_if = f'''{form[3]}_set.is_valid()'''
                s_5 = f'''
            for form in {form[3]}_set:
                form.save()'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ {form[3]}_set.as_p }}}}
        <hr>'''

            s1 = s1 + s_1
            s2 = s2 + s_2
            s3 = s3 + s_3
            s4 = s4 + c
            s5_if.append(s_5_if)
            s5 = s5 + s_5

            s6 = s6 + h
            s7 = s7 + p

            s2_create = s2_create + s_2_c
            s3_create = s3_create + s_3_c

            i += 1

        s5if = ''
        for i, s in enumerate(s5_if):
            if i == 0:
                s5if = 'if ' + s
            else:
                s5if = s5if + ' and ' + s
        s5if = s5if + ':'

        vs = [s0, s1, s2, s3, s4, s5, s5if, s7, s2_create, s3_create]
        
        return vs, s6

    # 构造views脚本（函数版本）
    def __construct_view_script(self, vs):

        # create view
        create_script_head = f'''
def {self.operand_name}_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {{}}
    '''

        create_script_body = f'''
    # inquire_forms''' + vs[0] + f'''
    # mutate_formsets''' + vs[1] + f'''
    # mutate_forms
    if request.method == 'POST':'''+ vs[8] + f'''
        ''' + vs[6] + vs[5] + f'''
            return redirect(reverse('index'))
    else:''' + vs[9] + f'''
    # context''' + vs[4]

        create_script_foot = f'''
    return render(request, '{self.operand_name}_create.html', context)'''

        # update view
        update_script_head = f'''
def {self.operand_name}_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])

    if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
        return redirect(reverse('index'))
    operation_proc.group.set([])  # 设置作业进程所属角色组为空
    # 构造作业开始消息参数
    operand_started.send(sender={self.operand_name}_update, operation_proc=operation_proc, ocode='rtr', operator=request.user)

    customer = operation_proc.customer
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {{}}
    '''

        update_script_body = vs[7] + f'''
    # inquire_forms''' + vs[0] + f'''
    # mutate_formsets''' + vs[1] + f'''
    # mutate_forms
    if request.method == 'POST':'''+ vs[2] + f'''
        ''' + vs[6] + vs[5] + f'''
            # 构造作业完成消息参数
            operand_finished.send(sender={self.operand_name}_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:''' + vs[3] + f'''
    # context''' + vs[4]

        update_script_foot = f'''
    context['proc_id'] = kwargs['id']
    return render(request, '{self.operand_name}_update.html', context)

    '''

        s = f'{create_script_head}{create_script_body}{create_script_foot}\n\n{update_script_head}{update_script_body}{update_script_foot}'
        return s

    # 构造html脚本
    def __construct_html_script(self, hs):
        script_head = f'''{{% extends "base.html" %}}

{{% load crispy_forms_tags %}}

{{% block content %}}
'''

        create_script_body = f'''
	<form action={{% url '{self.operand_name}_create_url' %}} method='POST' enctype='multipart/form-data'> 
		{{% csrf_token %}}
            ''' + hs

        update_script_body = f'''
	<form action={{% url '{self.operand_name}_update_url' proc_id %}} method='POST' enctype='multipart/form-data'> 
		{{% csrf_token %}}
            ''' + hs

        script_foot = f'''
		<input type="submit" value="提交" /> 
	</form>

{{% endblock %}}
'''

        s_create = f'{script_head}{create_script_body}{script_foot}'
        s_update = f'{script_head}{update_script_body}{script_foot}'
        return s_create, s_update

    # 构造urls脚本
    def __construct_url_script(self):
        return f'''
    path('{self.operand_name}/create', {self.operand_name}_create, name='{self.operand_name}_create_url'),
    path('{self.operand_name}/<int:id>/update', {self.operand_name}_update, name='{self.operand_name}_update_url'),'''


    # 构造index.html脚本
    def __construct_index_html_script(self):
        return f'''<a class='list-group-item' href='{{% url "{self.operand_name}_create_url" %}}'>
		{self.operand_label}
	</a>
        '''


########################################################################################################################
# 设计数据备份
########################################################################################################################
from django.forms.models import model_to_dict
from define.models import BoolField, CharacterField, NumberField, DTField, ChoiceField, RelateFieldModel, RelatedField, Component
from define_form.models import CombineForm
from define_operand.models import Service, ServicePackage, Event, Instruction, Role, DesignBackup
from define_dict.models import ManagedEntity, DicDetail

# 不备份再其他表新增内容时自动插入内容的表，RelateFieldModel
def design_backup(modeladmin, request, queryset):
    # 每个需要备份的model都需要在这里添加
    design_data = {
        'roles': [],
        'managedentities': [],
        'diclists': [],
        'dicdetails': [],
        # 'relatefieldmodels': [],
        'boolfields': [],
        'characterfields': [],
        'numberfields': [],
        'dtfields': [],
        'relatedfields': [],
        'choicefields': [],
        # 'components': [],
        'basemodels': [],
        'baseforms': [],
        'combineforms': [],
        'operations': [],
        'services': [],
        'service_packages': [],
        'instructions': [],
        'events': [],
    }

    for item in Role.objects.all():
        model = model_to_dict(item)
        design_data['roles'].append(model)

    for item in ManagedEntity.objects.all():
        design_data['managedentities'].append(model_to_dict(item))

    for item in DicList.objects.all():
        design_data['diclists'].append(model_to_dict(item))

    for item in DicDetail.objects.all():
        model = model_to_dict(item)
        model['diclist'] = item.diclist.dic_id
        if item.icpc:
            model['icpc'] = item.icpc.icpc_code
        design_data['dicdetails'].append(model)

    for item in BoolField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['boolfields'].append(model)

    for item in CharacterField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['characterfields'].append(model)

    for item in NumberField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['numberfields'].append(model)

    for item in DTField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['dtfields'].append(model)

    for item in RelatedField.objects.all():
        model = model_to_dict(item)
        model['related_content'] = item.related_content.relate_field_model_id
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['relatedfields'].append(model)

    for item in ChoiceField.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code
        design_data['choicefields'].append(model)

    # for item in Component.objects.all():
    #     design_data['components'].append(model_to_dict(item))

    for item in BaseModel.objects.all():
        model = model_to_dict(item)

        components = []
        for component in item.components.all():
            components.append(model_to_dict(component))
        model['components'] = components
        
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['managed_entity']:
            managed_entity_name = []
            for managed_entity in model['managed_entity']:
                managed_entity_name.append(managed_entity.entity_id)
            model['managed_entity'] = managed_entity_name

        design_data['basemodels'].append(model)

    for item in BaseForm.objects.filter(is_inquiry=True):
        model = model_to_dict(item)

        components = []
        for component in item.components.all():
            components.append(model_to_dict(component))
        model['components'] = components

        model['basemodel'] = item.basemodel.basemodel_id
        model.pop('meta_data')

        design_data['baseforms'].append(model)

    for item in CombineForm.objects.all():
        model = model_to_dict(item)

        forms = []
        for form in item.forms_new.all():
            _form = model_to_dict(form)
            forms.append(_form['baseform_id'])
        model['forms'] = forms
        model['forms_new'] = forms
        
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['managed_entity']:
            model['managed_entity'] = item.managed_entity.entity_id
        model.pop('meta_data')  # 去掉meta_data字段, 因为导入的时候会自动生成

        design_data['combineforms'].append(model)

    for item in Operation.objects.all():
        model = model_to_dict(item)

        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['forms']:
            model['forms'] = item.forms.combineform_id

        if model['group']:
            group_id = []
            for group in item.group.all():
                group_id.append(group.role_id)
            model['group'] = group_id

        design_data['operations'].append(model)


    for item in Service.objects.all():
        model = model_to_dict(item)
        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['first_operation']:
            model['first_operation'] = item.first_operation.operand_id

        if model['operations']:
            operations_name = []
            for operation in model['operations']:
                operations_name.append(operation.operand_id)
            model['operations'] = operations_name

        if model['group']:
            group_id = []
            for group in item.group.all():
                group_id.append(group.role_id)
            model['group'] = group_id

        design_data['services'].append(model)


    for item in ServicePackage.objects.all():
        model = model_to_dict(item)

        if item.name_icpc:
            model['name_icpc'] = item.name_icpc.icpc_code

        if model['first_service']:
            model['first_service'] = item.first_service.service_id

        if model['services']:
            services_id = []
            for service in item.sercices.all():
                services_id.append(service.service_id)
            model['services'] = services_id

        design_data['service_packages'].append(model)


    for item in Instruction.objects.all():
        model = model_to_dict(item)
        design_data['instructions'].append(model)

    for item in Event.objects.all():
        model = model_to_dict(item)
        model['operation'] = item.operation.operand_id
        if model['next']:
            next_operations = []
            for operation in item.next.all():
                next_operations.append(operation.operand_id)
            model['next'] = next_operations
        design_data['events'].append(model)


    # 写入数据库
    s = DesignBackup.objects.create(
        name = str(int(time())),
        code = json.dumps(design_data, indent=4, ensure_ascii=False),
    )
    print(f'设计数据备份成功, id: {s.id}')

design_backup.short_description = '备份设计数据'
