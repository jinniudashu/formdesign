#***********************************************************************************************************************
# 文件头设置
#***********************************************************************************************************************

service_models_file_head = '''from django.db import models

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, HsscBaseFormModel, Staff, Institution, Service, ServicePackage, Customer, CycleUnit, Medicine
from core.hsscbase_class import HsscBase

class CustomerSchedulePackage(HsscFormModel):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    
    class Meta:
        verbose_name = '安排服务包'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.servicepackage.label

class CustomerScheduleDraft(HsscBase):
    order = models.PositiveSmallIntegerField(default=100, verbose_name='顺序')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    cycle_unit = models.ForeignKey(CycleUnit, on_delete=models.CASCADE, default=1, blank=True, null=True, verbose_name='周期单位')
    cycle_frequency = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="每周期频次")
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="天数")
    Default_beginning_time = [(0, '无'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')]
    default_beginning_time = models.PositiveSmallIntegerField(choices=Default_beginning_time, default=0, verbose_name='执行时间基准')
    base_interval = models.DurationField(blank=True, null=True, verbose_name='基准间隔', help_text='例如：3 days, 22:00:00')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    
    class Meta:
        verbose_name = '服务项目安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label

class CustomerSchedule(HsscBase):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, verbose_name='客户')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    scheduled_draft = models.ForeignKey(CustomerScheduleDraft, on_delete=models.CASCADE, verbose_name='日程草案')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name='计划执行时间')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')

    class Meta:
        verbose_name = '客户服务日程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label


# **********************************************************************************************************************
# Service基本信息表单Model
# **********************************************************************************************************************
'''

service_admin_file_head = '''from django.contrib import admin
from django.shortcuts import redirect
import nested_admin

from core.admin import clinic_site
from core.signals import operand_finished
from core.business_functions import create_customer_service_log
from service.models import *


class HsscFormAdmin(admin.ModelAdmin):
    list_fields = ['name', 'id']
    exclude = ["hssc_id", "label", "name", "customer", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    view_on_site = False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # base_form = 'base_form'
        # extra_context['base_form'] = base_form
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # 把服务进程状态修改为已完成
        proc = obj.pid
        if proc:
            proc.update_state('RTC')

        import copy
        form_data1 = copy.copy(form.cleaned_data)
        form_data2 = copy.copy(form.cleaned_data)

        # 把表单内容存入CustomerServiceLog
        create_customer_service_log(form_data1, obj)

        # 发送服务作业完成信号
        print('发送操作完成信号, From service.admin.HsscFormAdmin.save_model：', obj.pid)
        operand_finished.send(sender=self, pid=obj.pid, request=request, form_data=form_data2)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        # 按照service.route_to的配置跳转
        redirect_option = obj.pid.service.route_to
        if redirect_option == 'CUSTOMER_HOMEPAGE':
            return redirect(obj.customer)
        else:
            return redirect('index')


class CustomerScheduleAdmin(admin.ModelAdmin):
    autocomplete_fields = ["scheduled_operator", ]
    list_display = ['service', 'scheduled_time', 'scheduled_operator']
    list_editable = ['scheduled_time', 'scheduled_operator']
    ordering = ('scheduled_time',)
clinic_site.register(CustomerSchedule, CustomerScheduleAdmin)
admin.site.register(CustomerSchedule, CustomerScheduleAdmin)

class CustomerScheduleInline(nested_admin.NestedTabularInline):
    model = CustomerSchedule
    extra = 0
    can_delete = False
    # verbose_name_plural = '服务日程安排'
    exclude = ["hssc_id", "label", "name", ]
    autocomplete_fields = ["scheduled_operator", ]

class CustomerScheduleDraftAdmin(HsscFormAdmin):
    autocomplete_fields = ["scheduled_operator", ]
    inlines = [CustomerScheduleInline]
clinic_site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)
admin.site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)

class CustomerScheduleDraftInline(nested_admin.NestedTabularInline):
    model = CustomerScheduleDraft
    inlines = [CustomerScheduleInline]
    extra = 0
    can_delete = False
    # verbose_name_plural = '服务项目安排'
    exclude = ["hssc_id", "label", "name", ]
    autocomplete_fields = ["scheduled_operator", ]

class CustomerSchedulePackageAdmin(HsscFormAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    fieldsets = ((None, {'fields': (('customer', 'servicepackage'), )}),)
    readonly_fields = ['customer', 'servicepackage']
    inlines = [CustomerScheduleDraftInline, ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        if instances:
            schedule_package = instances[0].schedule_package
            customer = schedule_package.customer
            from core.business_functions import get_services_schedule
            services_schedule = get_services_schedule(instances)
            print('services_schedule:', services_schedule)
            # 创建客户服务日程
            for service_schedule in services_schedule:
                CustomerSchedule.objects.create(
                    customer=customer,
                    schedule_package=schedule_package,
                    scheduled_draft=service_schedule['scheduled_draft'],
                    service=service_schedule['service'],
                    scheduled_time=service_schedule['scheduled_time'],
                    scheduled_operator=service_schedule['scheduled_operator'],
                )
            # 重定向到修改客户服务日程页面
            return redirect('/clinic/service/customerschedule/', pk=instances[0].pk)
            # return redirect('service:customer_schedule_edit', pk=instances[0].pk)

clinic_site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)
admin.site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)

# **********************************************************************************************************************
# Service表单Admin
# **********************************************************************************************************************
'''

# service\forms.py文件头
service_forms_file_head = '''from django.forms import ModelForm

'''


# forms/models.py文件头
forms_models_file_head = '''from django.db import models
from django.shortcuts import reverse
import json

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, Staff


'''

# forms/admin.py文件头
forms_admin_file_head = '''from django.contrib import admin
from .models import *

'''

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

    def natural_key(self):
        return self.value

    def save(self, *args, **kwargs):
        if self.label:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
            if self.name is None or self.name=='':
                self.name = "_".join(lazy_pinyin(self.label))
        super().save(*args, **kwargs)

'''

# 字典admin.py文件头
dict_admin_head = '''from django.contrib import admin
from core.admin import clinic_site
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

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.iname)

    def natural_key(self):
        return self.iname


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
from core.admin import clinic_site
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


# serializers.py文件头
serializers_head = '''from rest_framework import serializers
from .models import *
'''
