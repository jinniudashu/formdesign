from time import time
import json

from define.models import DicDetail, DicList
from define_operand.models import BuessinessForm, Operation
from define_backup.models import SourceCode
# 导入待生成脚本的文件头部设置
from define_backup.files_head_setting import models_file_head, admin_file_head, forms_file_head, modelform_footer, views_file_head, urls_file_head, index_html_file_head


# 生成作业脚本, 被define_operand.admin调用
def generate_source_code(modeladmin, request, queryset):
    source_code = {}
    source_code['dicts_models'], source_code['dicts_admin'] = DicList.export_dict.models_admin_script()
    source_code['dicts_data'] = DicDetail.export_dict.dict_data()
    
    source_code['models'] , source_code['admin'] = BuessinessForm.export_buessiness_form.models_admin_script()
    source_code['forms'] =  BuessinessForm.export_buessiness_form.forms_script()
    # source_code['views'] , source_code['urls'], source_code['templates'], source_code['operand_views'] = generate_views_urls_templates_code()

    # 写入数据库
    s = SourceCode.objects.create(
        name = str(int(time())),
        code = json.dumps(source_code, ensure_ascii=False),
    )
    print(f'写入数据库成功, id: {s.id}')

generate_source_code.short_description = '生成作业脚本'


###################################################################################################################
# generate forms.py script
###################################################################################################################
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
