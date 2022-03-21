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
    creater = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="创建人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
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