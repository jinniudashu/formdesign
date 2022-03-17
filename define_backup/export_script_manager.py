from django.db import models
from django.forms.models import model_to_dict
import json


# 自定义管理器：导出字典脚本，字典数据
class ExportDictManager(models.Manager):
    # 导出字典models.py, admin.py脚本
    def models_admin_script(self, fields=None):
        if self.model.__name__ != 'DicList':
            return 'Only DicList can use this function'
        else:
            models_script = dict_models_head
            admin_script = dict_admin_head            
            dicts = self.all()

            for dict in dicts:
                name = dict.name.capitalize()

                # 生成model脚本
                _model_script = f'''
class {name}(DictBase):
    class Meta:
        verbate_name = '{dict.label}'
        verbate_name_plural = verbate_name'''
                models_script = f'{models_script}\n\n{_model_script}'

                # 生成admin脚本
                _admin_script = f'''
@admin.register({name})
class {name}Admin(admin.ModelAdmin):{dict_admin_content}'''
                admin_script = f'{admin_script}\n\n{_admin_script}'

            return models_script, admin_script
    
    # 导出字典Json数据
    def dict_data(self, fields=None):
        if self.model.__name__ != 'DicDetail':
            return 'Only DicDetail can use this function'
        else:
            dict_data = []

            # 构造字典明细数据
            for item in self.all():
                item_dict = model_to_dict(item)
                item_dict['id'] = None
                if item_dict['icpc']:
                    item_dict['icpc'] = item.icpc.icpc_code
                item_dict['diclist'] = item.diclist.hssc_id
                dict_data.append(item_dict)

            return dict_data

# 自定义管理器：导出models.py、admin.py脚本
class ExportBuessinessFormManager(models.Manager):
    # 导出业务表单models.py, admin.py脚本
    def models_admin_script(self, fields=None):
        if self.model.__name__ != 'BuessinessForm':
            return 'Only BuessinessForm can use this function'
        else:
            # construct models.py and admin.py script
            models_script = models_file_head
            admin_script =  admin_file_head
            for form in self.all():
                _s = self.__CreateModelScript(form)
                _m, _a = _s.create_script()
                models_script = models_script + _m
                admin_script = admin_script + _a

            return models_script, admin_script

    # 导出业务表单forms.py脚本
    def forms_script(self, fields=None):
        if self.model.__name__ != 'BuessinessForm':
            return 'Only BuessinessForm can use this function'
        else:
            # construct forms.py script
            forms_script = forms_file_head
            for form in self.all():
                _s = self.__CreateFormScript(form)
                _f = _s.create_script()
                forms_script = forms_script + _f

            return forms_script

    # 导出业务表单views.py，template.html, urls.py, index.html脚本
    def views_urls_templates_script(self, fields=None):
        if self.model.__name__ != 'BuessinessForm':
            return 'Only BuessinessForm can use this function'
        else:
            # create views.py, template.html, urls.py
            views_script = views_file_head
            urls_script = urls_file_head
            templates_code = []
            index_html_script = index_html_file_head

            for form in self.all():
                _s = self.__CreateViewScript(form)
                vs, us, chs, uhs, ihs = _s.create_script()
                
                # construct views script
                views_script = views_script + vs
                # construct urls script
                urls_script = urls_script + us
                # create templates.html
                templates_code.append({f'{form.name}_create.html': chs})
                templates_code.append({f'{form.name}_update.html': uhs})
                # construct index.html script
                index_html_script = index_html_script + ihs

            templates_code.append({'index.html': f"{index_html_script}'\n</section>\n{{% endblock %}}'"})

            return views_script, f'{urls_script}\n]', templates_code

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
            self.model = form.basemodel.name.capitalize()
            self.style = form.style
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
            model = {self.model}
            fields = [{self.fields}]
            {self.widgets}
            '''

            return f'{head_script}{body_script}{form_footer}'

    class __CreateViewScript:
        def __init__(self, obj):
            self.operand_name = obj.name
            self.operand_label = obj.label
            self.managed_entity = obj.form.managed_entity
            form = json.loads(obj.form.meta_data)

            self.view_name = self.operand_name.capitalize() + '_CreateView'
            self.template_name = self.operand_name + '_edit.html'
            self.success_url = '/'
            # 如果作业不包含可修改表单，self.mutate_forms=[]，会报错IndexError: list index out of range
            self.form_class = self.mutate_forms[0][0].capitalize() + '_ModelForm'

            self.url = self.operand_name + '_update_url'

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


#***********************************************************************************************************************
# 文件头设置
#***********************************************************************************************************************

# models.py文件头
models_file_head = '''from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from time import time
from datetime import date
from django.utils import timezone

from icpc.models import *
from dictionaries.models import *
from core.models import Staff, Customer, Operation_proc

class HsscBuessinessFormBase(models.Model):
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.customer)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{{int(time())}}'
        super().save(*args, **kwargs)

'''

# admin.py文件头
admin_file_head = '''from django.contrib import admin
from .models import *
    '''

# forms.py文件头
forms_file_head = '''from django.forms import ModelForm, Form,  widgets, fields, RadioSelect, Select, CheckboxSelectMultiple, CheckboxInput, SelectMultiple, NullBooleanSelect
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *
'''

# form固定内容
form_footer = '''
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug
'''

# views.py文件头
views_file_head = f'''from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory
import json

from core.models import Operation_proc, Staff, Customer
from core.signals import operand_started, operand_finished

from django.contrib.messages.views import SuccessMessageMixin
from forms.utils import *

from forms.models import *
from forms.forms import *

class Index_view(ListView):
    model = Operation_proc
    template_name = 'index.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Operation_proc.objects.exclude(state=4))

    def get_context_data(self, **kwargs):
        # 如果用户当前未登录，request.user将被设置为AnonymousUser。用user.is_authenticated()判断用户登录状态：
        operator=Staff.objects.get(user=self.request.user)
        group = Group.objects.filter(user=self.request.user)
        # 获取当前用户所属角色组的所有作业进程
        procs = Operation_proc.objects.exclude(state=4).filter(Q(group__in=group) | Q(operator=operator)).distinct()

        todos = []
        for proc in procs:
            todo = {{}}
            todo['operation'] = proc.operation.label
            todo['url'] = f'{{proc.operation.name}}_update_url'
            todo['proc_id'] = proc.id
            todos.append(todo)
        context = super().get_context_data(**kwargs)
        context['todos'] = todos
        return context

'''

# urls.py文件头
urls_file_head = '''from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),'''

# index.html文件头
index_html_file_head = f'''{{% extends "base.html" %}}

{{% block content %}}

<br>

<h5>当前任务</h5>
	<section class="list-group">
	{{% for todo in todos %}}
		<a class="list-group-item" href="{{% url todo.url todo.proc_id %}}">
		{{{{ todo.operation }}}}
		</a>
	{{% endfor %}}
	</section>

<br>

<hr>

<br>

<h5>系统菜单</h5>

<section class="list-group">
'''

# 字典models.py文件头
dict_models_head = '''from django.db import models

class DictBase(models.Model):
    label = models.CharField(max_length=255, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name="值")
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    class Meta:
        abstract = True

    def __str__(self):
        return self.value

'''

# 字典admin.py文件头
dict_admin_head = '''from django.contrib import admin
from .models import *

'''

# 字典admin固定内容
dict_admin_content = '''
    search_fields = ['value', 'pym']
    list_display = ["value"]
'''