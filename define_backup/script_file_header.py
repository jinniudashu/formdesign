#***********************************************************************************************************************
# 文件头设置
#***********************************************************************************************************************

service_models_file_head = '''from django.db import models
from django.shortcuts import reverse
import json

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, Role, Staff, OperationProc
from entities.models import *

@receiver(post_save, sender=OperationProc)
def operation_proc_created(sender, instance, created, **kwargs):
    # 创建服务进程里使用的表单实例, 将form_slugs保存到进程实例中
    if created and instance.state == 0:  # 系统保留作业(state=4)不创建model进程
        model_name = instance.service.name.capitalize()
        print('创建表单实例:', model_name)
        form = eval(model_name).objects.create(
            customer=instance.customer,
            creater=instance.operator,
            pid=instance,
            cpid=instance.contract_service_proc,
        )
        # 更新OperationProc服务进程的入口url
        instance.entry = f'/clinic/service/{instance.service.name.lower()}/{form.id}/change'
        instance.save()


'''
service_admin_file_head = '''# from django.forms import ModelForm, Select, CheckboxSelectMultiple
from django.shortcuts import redirect
from django.contrib import admin

from hssc.site import clinic_site
from service.models import *
# from forms.models import A6203


# class A6203_ModelForm(ModelForm):
#     class Meta:
#         model = A6203
#         fields = ['characterfield_name', 'characterhssc_identification_number', 'characterfield_resident_file_number', 'characterfield_family_address', 'characterfield_contact_number', 'characterfield_medical_ic_card_number', 'datetimefield_date_of_birth', 'relatedfield_gender', 'relatedfield_nationality', 'relatedfield_marital_status', 'relatedfield_education', 'relatedfield_occupational_status', 'relatedfield_medical_expenses_burden', 'relatedfield_type_of_residence', 'relatedfield_blood_type', 'relatedfield_signed_family_doctor', 'relatedfield_family_relationship', ]
#         widgets = {'relatedfield_gender': Select, 'relatedfield_nationality': Select, 'relatedfield_marital_status': Select, 'relatedfield_education': Select, 'relatedfield_occupational_status': Select, 'relatedfield_medical_expenses_burden': CheckboxSelectMultiple, 'relatedfield_type_of_residence': Select, 'relatedfield_blood_type': Select, 'relatedfield_signed_family_doctor': Select, 'relatedfield_family_relationship': Select, }

class HsscFormAdmin(admin.ModelAdmin):
    exclude = ["hssc_id", "label", "name", "customer", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", ]
    view_on_site = False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # base_form = A6203_ModelForm(prefix="base_form")
        base_form = 'base_form'
        extra_context['base_form'] = base_form
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        return redirect('/clinic/')

'''

# forms/models.py文件头
forms_models_file_head = '''from django.db import models
from django.shortcuts import reverse
import json

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, Role, Staff, OperationProc
from entities.models import *


@receiver(post_save, sender=OperationProc)
def operation_proc_created(sender, instance, created, **kwargs):
    # 创建服务进程里使用的表单实例, 将form_slugs保存到进程实例中
    if created:
        form_slugs = []
        for form in instance.service.buessiness_forms.all():
            form_class_name = form.name.capitalize()
            print('创建表单实例:', form_class_name)
            form = eval(form_class_name).objects.create(
                customer=instance.customer,
                creater=instance.operator,
                pid=instance,
                cpid=instance.contract_service_proc,
            )
            form_slugs.append({'form_name': form_class_name, 'slug': form.slug})
        instance.form_slugs = json.dumps(form_slugs, ensure_ascii=False, indent=4)
        instance.save()


'''

# forms/admin.py文件头
forms_admin_file_head = '''from django.contrib import admin
from .models import *

from hssc.site import clinic_site
from forms.forms import A6203_ModelForm

class HsscFormAdmin(admin.ModelAdmin):
    exclude = ('hssc_id','slug')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        base_form = A6203_ModelForm(prefix="base_form")
        extra_context['base_form'] = base_form
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

'''

# forms/forms.py文件头
forms_forms_file_head = '''from django.forms import ModelForm, Form,  widgets, fields, RadioSelect, Select, CheckboxSelectMultiple, CheckboxInput, SelectMultiple, NullBooleanSelect
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

from core.models import OperationProc, Staff, Customer
from core.utils import SendSignalsMixin
from forms.utils import *
from forms.models import *
from forms.forms import *


class Index_view(ListView):
    model = OperationProc
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # 如果用户当前未登录，request.user将被设置为AnonymousUser。用user.is_authenticated()判断用户登录状态：
        operator=User.objects.get(username=self.request.user).customer
        role = operator.staff.role.all()
        # 获取当前用户所属角色的所有作业进程
        procs = OperationProc.objects.exclude(state=4).filter(Q(role__in=role) | Q(operator=operator)).distinct()

        todos = []
        for proc in procs:
            todo = {{}}
            todo['operation'] = proc.service.label
            todo['url'] = f'{{proc.service.name}}_update_url'
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
from pypinyin import Style, lazy_pinyin


class DictBase(models.Model):
    label = models.CharField(max_length=255, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name="值")
    icpc = models.CharField(max_length=5, null=True, blank=True, verbose_name="ICPC编码")
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    class Meta:
        abstract = True

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        if self.label:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
            if self.name is None or self.name=='':
                self.name = "_".join(lazy_pinyin(self.label))
        super().save(*args, **kwargs)'''

# 字典admin.py文件头
dict_admin_head = '''from django.contrib import admin
from hssc.site import clinic_site
from .models import *
'''

# 字典admin固定内容
dict_admin_content = '''
    search_fields = ['value', 'pym']
    list_display = ["value"]
'''

# ICPC字典models.py文件头
icpc_models_head = '''
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from pypinyin import Style, lazy_pinyin

class IcpcBase(models.Model):
    icpc_code = models.CharField(max_length=5, unique=True, blank=True, null=True, verbose_name="icpc码")
    icode = models.CharField(max_length=3, blank=True, null=True, verbose_name="分类码")
    iname = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    iename = models.CharField(max_length=255, blank=True, null=True, verbose_name="English Name")
    include = models.CharField(max_length=1024, blank=True, null=True, verbose_name="包含")
    criteria = models.CharField(max_length=1024, blank=True, null=True, verbose_name="准则")
    exclude = models.CharField(max_length=1024, blank=True, null=True, verbose_name="排除")
    consider = models.CharField(max_length=1024, blank=True, null=True, verbose_name="考虑")
    icd10 = models.CharField(max_length=8, blank=True, null=True, verbose_name="ICD10")
    icpc2 = models.CharField(max_length=10, blank=True, null=True, verbose_name="ICPC2")
    note = models.CharField(max_length=1024, blank=True, null=True, verbose_name="备注")
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    def __str__(self):
        return str(self.iname)

    class Meta:
        abstract = True


# ICPC子类抽象类
class IcpcSubBase(IcpcBase):
    def save(self, *args, **kwargs):
        if self.iname:
            self.pym = ''.join(lazy_pinyin(self.iname, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# ICPC总表
class Icpc(IcpcBase):
    subclass = models.CharField(max_length=255, blank=True, null=True, verbose_name="ICPC子类")

    class Meta:
        verbose_name = "ICPC总表"
        verbose_name_plural = verbose_name
'''

icpc_models_post_save = '''
def icpc_post_save_handler(sender, instance, created, **kwargs):
	if created:
		Icpc.objects.create(
			icpc_code=instance.icpc_code,
			icode=instance.icode,
			iname=instance.iname,
			iename=instance.iename,
			include=instance.include,
			criteria=instance.criteria,
			exclude=instance.exclude,
			consider=instance.consider,
			icd10=instance.icd10,
			icpc2=instance.icpc2,
			note=instance.note,
			pym=instance.pym,
			subclass=instance._meta.object_name
		)
	else:
		Icpc.objects.filter(icpc_code=instance.icpc_code).update(
			icode=instance.icode,
			iname=instance.iname,
			iename=instance.iename,
			include=instance.include,
			criteria=instance.criteria,
			exclude=instance.exclude,
			consider=instance.consider,
			icd10=instance.icd10,
			icpc2=instance.icpc2,
			note=instance.note,
			pym=instance.pym,
			subclass=instance._meta.object_name
		)
'''

icpc_models_post_delete = '''
def icpc_post_delete_handler(sender, instance, **kwargs):
	Icpc.objects.filter(icpc_code=instance.icpc_code).delete()
'''

# ICPC字典admin.py文件头
icpc_admin_head = '''from django.contrib import admin
from hssc.site import clinic_site
from .models import *

@admin.register(Icpc)
class IcpcAdmin(admin.ModelAdmin):
    list_display = ["icpc_code", "icode", "iname", "pym", "subclass"]
    search_fields=["iname", "pym", "icpc_code", "icode"]
    ordering = ["icpc_code"]
    readonly_fields = ['icpc_code','icode','iname','iename','include','criteria','exclude','consider','icd10','icpc2','note','pym', 'subclass']
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class SubIcpcAdmin(admin.ModelAdmin):
    list_display = ["icpc_code", "icode", "iname", "pym"]
    search_fields=["iname", "pym", "icpc_code", "icode"]
    ordering = ["icpc_code"]
    readonly_fields = ['icpc_code','icode','iname','iename','include','criteria','exclude','consider','icd10','icpc2','note','pym']
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False'''