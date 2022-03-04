from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, m2m_changed, post_save
import json
import uuid
from django.contrib.auth.models import Group

from pypinyin import lazy_pinyin

from define_icpc.models import Icpc
from define_form.models import CombineForm
from .keyword_search import keyword_search


# 角色表
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="角色名")
    label = models.CharField(max_length=255, verbose_name="显示名称")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="角色描述")
    role_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="角色ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.role_id is None:
            self.role_id = uuid.uuid1()
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"
        ordering = ['id']


# 作业基础信息表
class Operation(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="作业名称")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
    forms = models.ForeignKey(CombineForm, on_delete=models.CASCADE, null=True, blank=True, verbose_name="作业表单")
    Operation_priority = [
        (0, '0级'),
        (1, '紧急'),
        (2, '优先'),
        (3, '一般'),
    ]
    execute_datetime = models.DateTimeField(blank=True, null=True, verbose_name='执行时间')
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    group = models.ManyToManyField(Role, blank=True, verbose_name="作业角色")
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    time_limits = models.DurationField(blank=True, null=True, verbose_name='完成时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')
    operand_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="作业ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.operand_id is None:
            self.operand_id = uuid.uuid1()
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = "作业"
        ordering = ['id']


# 单元服务类型信息表
class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=255, verbose_name="显示名称")
    first_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='first_operation', blank=True, null=True, verbose_name="起始作业")
    operations = models.ManyToManyField(Operation, blank=True, verbose_name="包含作业")
    execute_datetime = models.DateTimeField(blank=True, null=True, verbose_name='执行时间')
    Operation_priority = [
        (0, '0级'),
        (1, '紧急'),
        (2, '优先'),
        (3, '一般'),
    ]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    group = models.ManyToManyField(Role, blank=True, verbose_name="服务角色")
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    time_limits = models.DurationField(blank=True, null=True, verbose_name='完成时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')
    service_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="单元服务ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.service_id is None:
            self.service_id = uuid.uuid1()
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "单元服务"
        verbose_name_plural = "单元服务"
        ordering = ['id']


class ServicePackage(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=255, verbose_name="显示名称")
    first_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='first_service', blank=True, null=True, verbose_name="起始服务")
    services = models.ManyToManyField(Service, blank=True, verbose_name="包含服务")
    execute_datetime = models.DateTimeField(blank=True, null=True, verbose_name='执行时间')
    service_package_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="服务包ID")

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if self.service_package_id is None:
            self.service_package_id = uuid.uuid1()
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "服务包"
        verbose_name_plural = "服务包"
        ordering = ['id']


# 作业事件表
# # 默认事件：xx作业完成--系统作业名+"_operation_completed"
class Event(models.Model):
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="事件名")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='from_oid', verbose_name="所属作业")
    expression = models.TextField(max_length=1024, blank=True, null=True, default='completed', verbose_name="表达式", 
        help_text='''
        说明：<br>
        1. 作业完成事件: completed<br>
        2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>
        3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"
        ''')
    next_operations = models.ManyToManyField(Operation, through='EventRoute', verbose_name="后续作业")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="事件描述")
    parameters = models.CharField(max_length=1024, blank=True, null=True, verbose_name="检查字段")
    fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="可用字段")
    event_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="事件ID")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.event_id is None:
            self.event_id = uuid.uuid1()

        # 自动为事件名加作业名为前缀
        if self.operation.name not in self.name:
            self.name = f'{self.operation.name}_{self.name}'
            # 保留字：作业完成事件，自动填充expression为'completed'
            if self.name == f'{self.operation.name}_completed':
                self.expression = 'completed'

        if self.operation.forms:
            # 生成fields
            forms = json.loads(self.operation.forms.meta_data)
            fields = []
            field_names = []
            for form in forms:
                form_name = form['basemodel']
                _fields = form['fields']
                for _field in _fields:
                    field_name = form_name + '-' + _field['name']
                    field_label = _field['label']
                    field_type = _field['type']
                    field_app_label = _field.get('app_label')
                    field_names.append(field_name)
                    fields.append(str((field_name, field_label, field_type, field_app_label)))

            self.fields = '\n'.join(fields)

            # 生成表达式参数列表
            if self.expression and self.expression != 'completed':
                _form_fields = keyword_search(self.expression, field_names)
                self.parameters = ', '.join(_form_fields)

        super().save(*args, **kwargs)


# 作业间隔规则表
class OperandIntervalRule(models.Model):
    label = models.CharField(max_length=255, verbose_name="规则名称")
    name = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name="name")
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔规则')
    interval = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="说明")
    operand_interval_rule_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="间隔规则ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.operand_interval_rule_id is None:
            self.operand_interval_rule_id = uuid.uuid1()
        if self.name is None:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "间隔规则"
        verbose_name_plural = "间隔规则"
        ordering = ['id']


# 事件路由作业表
class EventRoute(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="事件")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="后续作业")
    is_specified = models.BooleanField(default=False, verbose_name="规定作业")  # 默认为：推荐作业
    interval_rule = models.ForeignKey(OperandIntervalRule, on_delete=models.CASCADE, blank=True, null=True, verbose_name="间隔规则")
    event_route_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="事件路由ID")

    def __str__(self):
        return str(self.event) + '--' + str(self.operation)

    class Meta:
        verbose_name = "事件后续作业"
        verbose_name_plural = "事件后续作业"
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.event_route_id is None:
            self.event_route_id = uuid.uuid1()
        super().save(*args, **kwargs)


# 指令表
class Instruction(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name="指令名称")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
    code = models.CharField(max_length=10, verbose_name="指令代码")
    func = models.CharField(max_length=100, verbose_name="操作函数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="指令描述")
    instruction_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="指令ID")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.instruction_id is None:
            self.instruction_id = uuid.uuid1()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "指令"
        verbose_name_plural = "指令"
        ordering = ['id']


# 事件指令程序表
class Event_instructions(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True, verbose_name="事件")
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, verbose_name="指令")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="指令序号")
    params = models.CharField(max_length=255, blank=True, null=True, verbose_name="创建作业")

    def __str__(self):
        return self.instruction.name

    class Meta:
        verbose_name = "事件指令集"
        verbose_name_plural = "事件指令集"
        ordering = ['event', 'order']


# 输出脚本
class SourceCode(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="版本")
    label = models.CharField(max_length=255, verbose_name="版本名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    code = models.TextField(verbose_name="源代码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "输出脚本"
        verbose_name_plural = "输出脚本"
        ordering = ['id']


# 设计数据备份
class DesignBackup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="版本")
    label = models.CharField(max_length=255, verbose_name="版本名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    code = models.TextField(verbose_name="源代码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "设计备份"
        verbose_name_plural = "设计备份"
        ordering = ['id']


# ********************
# 作业进程设置
# ********************
# 监视事件路由表EventRoute变更，变更事件后续作业时，同步变更事件指令表Event_instructions的内容
@receiver(post_save, sender=EventRoute)
def event_route_post_save_handler(sender, instance, created, **kwargs):
    if created:
        # 设定指令为 create_operation_proc
        instruction_create_operation_proc = Instruction.objects.get(name='create_operation_proc')
        Event_instructions.objects.create(
            event=instance.event,
            instruction=instruction_create_operation_proc,
            params=instance.operation.name,    # 用后续作业name作为指令参数
        )

@receiver(post_delete, sender=EventRoute)
def event_route_post_delete_handler(sender, instance, **kwargs):
    Event_instructions.objects.filter(event=instance.event, params=instance.operation.name).delete()
