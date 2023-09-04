#***********************************************************************************************************************
# 文件头设置
#***********************************************************************************************************************

service_models_file_head = '''from django.db import models

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, OperationProc, VirtualStaff, Staff, Institution, Service, ServicePackage, Customer, CycleUnit, Medicine
from core.hsscbase_class import HsscBase

from django.db.models import Q, F
from datetime import datetime, timedelta
from django.utils import timezone

from pypinyin import lazy_pinyin

class CustomerSchedulePackage(HsscFormModel):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    start_time = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='开始时间')

    class Meta:
        verbose_name = '安排服务包'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.servicepackage.label

class CustomerScheduleList(HsscFormModel):
    plan_serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='服务计划')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    is_ready = models.BooleanField(default=False, verbose_name='已生成schedules')
    
    class Meta:
        verbose_name = '客户服务计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.plan_serial_number

class CustomerScheduleDraft(HsscBase):
    order = models.PositiveSmallIntegerField(default=100, verbose_name='顺序')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    cycle_unit = models.ForeignKey(CycleUnit, on_delete=models.CASCADE, default=1, blank=True, null=True, verbose_name='周期单位')
    cycle_frequency = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="每周期频次")
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="天数")
    Default_beginning_time = [(0, '指定开始时间'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')]
    default_beginning_time = models.PositiveSmallIntegerField(choices=Default_beginning_time, default=0, verbose_name='执行时间基准')
    base_interval = models.DurationField(blank=True, null=True, verbose_name='基准间隔', help_text='例如：3 days, 22:00:00')
    # 根据当前service的值动态筛选有服务权限的服务人员
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')
    # 优先操作人员仅限工作小组
    priority_operator = models.ForeignKey(VirtualStaff, on_delete=models.SET_NULL, limit_choices_to={'is_workgroup': True}, blank=True, null=True, verbose_name="优先操作员")
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    
    class Meta:
        verbose_name = '服务项目安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label

class CustomerSchedule(HsscFormModel):
    customer_schedule_list = models.ForeignKey(CustomerScheduleList, null=True, blank=True, on_delete=models.CASCADE, verbose_name='服务计划')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, blank=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name='计划执行时间')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='计划服务人员')
    priority_operator = models.ForeignKey(VirtualStaff, on_delete=models.SET_NULL, limit_choices_to={'is_workgroup': True}, blank=True, null=True, verbose_name="优先操作员")
    reference_operation = models.ManyToManyField(OperationProc, blank=True, limit_choices_to=Q(customer=F('customer'), service__service_type=2, created_time__gte=datetime.now() - timedelta(days=7)), verbose_name='引用表单')
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    is_assigned = models.BooleanField(default=False, verbose_name='已生成任务')

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

from core.admin import clinic_site
from core.signals import operand_finished
from core.business_functions import get_services_schedule, create_customer_service_log
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

        if any(key.endswith('-TOTAL_FORMS') for key in request.POST):
            # 表单数据包含InlineModelAdmin 实例, 由save_formset发送服务作业完成信号
            # 保存obj到request for later retrieval in save_formset
            request._saved_obj = obj                
        else: # 表单数据不包含InlineModelAdmin 实例, 由save_model发送服务作业完成信号
            # 把表单内容存入CustomerServiceLog
            log = create_customer_service_log(form.cleaned_data, None, obj)

            # 把服务进程状态修改为已完成
            proc = obj.pid
            if proc:
                proc.update_state('RTC')

            print('操作完成(save_model)：', obj.pid)
            operand_finished.send(sender=self, pid=obj.pid, request=request, form_data=form.cleaned_data, formset_data=None)

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

        # Retrieve obj from the request
        obj = getattr(request, '_saved_obj', None)

        form_data = form.cleaned_data
       # 使用formset.forms获取每个form的实例
        # formset_data = [form.instance for form in formset.forms]
        formset_data = formset.cleaned_data

        # 把表单明细内容存入CustomerServiceLog
        log = create_customer_service_log(form_data, formset_data, obj)

        # 把服务进程状态修改为已完成
        proc = obj.pid
        if proc:
            proc.update_state('RTC')

        print('操作完成(save_formset)：', obj.pid)
        operand_finished.send(sender=self, pid=obj.pid, request=request, form_data=form_data, formset_data=formset_data)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        # # 如果是创建服务包计划，保存后跳转到修改服务计划列表的页面
        # if obj.__class__.__name__ == 'CustomerSchedulePackage':
        #     schedule_list = CustomerScheduleList.objects.get(schedule_package=obj)
        #     print('Change CustomerSchedulePackage', obj, 'to', schedule_list)
        #     return redirect(f'/clinic/service/customerschedulelist/{schedule_list.id}/change/')

        # 按照service.route_to的配置跳转
        if obj.pid.service.route_to == 'CUSTOMER_HOMEPAGE':
            return redirect(obj.customer)
        else:
            return redirect('index')


class CustomerScheduleAdmin(HsscFormAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym", 'customer_schedule_list', 'schedule_package', ]
    autocomplete_fields = ["scheduled_operator", ]
    list_display = ['customer', 'service', 'scheduled_time', 'scheduled_operator', 'priority_operator', 'pid', 'overtime', 'is_assigned', 'operator', 'creater', ]
    list_editable = ['scheduled_time', 'scheduled_operator', 'overtime', 'is_assigned']
    readonly_fields = ['customer', 'service']
    filter_horizontal = ('reference_operation',)
    ordering = ('scheduled_time',)

clinic_site.register(CustomerSchedule, CustomerScheduleAdmin)
admin.site.register(CustomerSchedule, CustomerScheduleAdmin)

class CustomerScheduleInline(admin.TabularInline):
    model = CustomerSchedule
    extra = 0
    can_delete = False
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", 'customer', 'schedule_package', 'is_assigned']
    autocomplete_fields = ["scheduled_operator", ]


class CustomerScheduleListAdmin(admin.ModelAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    fieldsets = ((None, {'fields': (('customer', 'plan_serial_number', ), )}),)
    readonly_fields = ['customer', 'plan_serial_number', ]
    inlines = [CustomerScheduleInline, ]

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        return redirect(obj.customer)

clinic_site.register(CustomerScheduleList, CustomerScheduleListAdmin)
admin.site.register(CustomerScheduleList, CustomerScheduleListAdmin)


class CustomerScheduleDraftAdmin(admin.ModelAdmin):
    autocomplete_fields = ["scheduled_operator", ]
clinic_site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)
admin.site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)

from django.forms import ModelForm
class CustomCustomerScheduleDraftForm(ModelForm):
    class Meta:
        model = CustomerScheduleDraft
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 如果这个表单的实例已经有一个选择的service
        if self.instance and self.instance.service:
            from core.models import Staff
            # 获取所有该service关联的roles
            roles = self.instance.service.role.all()
            # 过滤选择Staff.role在roles里的员工
            self.fields['scheduled_operator'].queryset = Staff.objects.filter(role__in=roles).distinct()

class CustomerScheduleDraftInline(admin.TabularInline):
    model = CustomerScheduleDraft
    form = CustomCustomerScheduleDraftForm
    extra = 0
    can_delete = False
    # verbose_name_plural = '服务项目安排'
    exclude = ["hssc_id", "label", "name", ]
    # autocomplete_fields = ["scheduled_operator", ]

    def get_queryset(self, request):
        # 重写get_queryset方法，设置缺省overtime为服务的overtime
        qs = super().get_queryset(request)
        for item in qs:
            item.overtime = item.service.overtime
            item.save()
        return qs

class CustomerSchedulePackageAdmin(HsscFormAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    fieldsets = ((None, {'fields': (('customer', 'servicepackage'), 'start_time' )}),)
    readonly_fields = ['customer', 'servicepackage']
    inlines = [CustomerScheduleDraftInline, ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        instances = formset.queryset

        if instances:
            schedule_package = instances[0].schedule_package
            schedules = get_services_schedule(instances, schedule_package.start_time)

            # 生成CustomerScheduleList记录
            schedule_list = CustomerScheduleList.objects.create(
                customer = schedule_package.customer,
                operator = schedule_package.operator,
                creater = schedule_package.creater,
                plan_serial_number = schedule_package.servicepackage.label + '--' + schedule_package.created_time.strftime('%Y-%m-%d') + '--' + schedule_package.operator.name,
                schedule_package = schedule_package,
                is_ready = False
            )

            # 创建客户服务日程
            for schedule in schedules:
                CustomerSchedule.objects.create(
                    customer_schedule_list = schedule_list,
                    customer=schedule_package.customer,
                    operator=schedule_package.operator,
                    creater=schedule_package.creater,
                    schedule_package=schedule_package,
                    service=schedule['service'],
                    scheduled_time=schedule['scheduled_time'],
                    scheduled_operator=schedule['scheduled_operator'],
                    priority_operator=schedule['priority_operator'],
                    overtime=schedule['overtime'],
                    pid=schedule_package.pid
                )

            # 更新服务进程entry为'customerschedulelist/id/change/'
            schedule_list.schedule_package.pid.entry = f'/clinic/service/customerschedulelist/{schedule_list.id}/change'
            schedule_list.schedule_package.pid.save()

            schedule_list.is_ready = True  # 完成一次创建服务包计划安排事务
            schedule_list.save()

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

clinic_site.register(Icpc, IcpcAdmin)

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


# template.html文件头, 文件尾
template_head = '''{% extends "admin/change_form.html" %}

{% block extrahead %}
{{ block.super }}
'''

template_end = '''
{% endblock %}'''