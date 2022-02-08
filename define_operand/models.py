from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, m2m_changed
import json
from django.contrib.auth.models import Group

from pypinyin import lazy_pinyin

from define_form.models import CombineForm
from .keyword_search import keyword_search


# 角色表
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="角色名")
    label = models.CharField(max_length=255, verbose_name="显示名称")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="角色描述")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"
        ordering = ['id']


# 作业信息表
class Operation(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="作业名称")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
    forms = models.ForeignKey(CombineForm, on_delete=models.CASCADE, null=True, blank=True, verbose_name="组合视图")
    # forms = models.JSONField(null=True, blank=True, verbose_name="视图元数据")
    # icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
    Operation_priority = [
        (0, '0级'),
        (1, '紧急'),
        (2, '优先'),
        (3, '一般'),
    ]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    group = models.ManyToManyField(Role, verbose_name="作业角色")
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

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = "作业"
        ordering = ['id']


# 服务类型信息表
class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    label = models.CharField(max_length=255, verbose_name="显示名称")
    # icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
    first_operation = models.ForeignKey(Operation, on_delete=models.SET_NULL, related_name='first_operation',blank=True, null=True, verbose_name="起始作业")
    
    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = "服务"
        ordering = ['id']


# 作业事件表
# # 默认事件：xx作业完成--系统作业名+"_operation_completed"
class Event(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="事件名")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='from_oid', verbose_name="所属作业")
    next = models.ManyToManyField(Operation, verbose_name="后续作业")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="事件描述")
    expression = models.TextField(max_length=1024, blank=True, null=True, default='completed', verbose_name="表达式", 
        help_text='''
        说明：<br>
        1. 作业完成事件: completed<br>
        2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>
        3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"
        ''')
    parameters = models.CharField(max_length=1024, blank=True, null=True, verbose_name="检查字段")
    fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="可用字段")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"
        ordering = ['id']

    def save(self, *args, **kwargs):
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

                    field_names.append(field_name)
                    fields.append(str((field_name, field_label, field_type)))

            self.fields = '\n'.join(fields)

            # 生成表达式参数列表
            if self.expression and self.expression != 'completed':
                _form_fields = keyword_search(self.expression, field_names)
                self.parameters = ', '.join(_form_fields)
                print('Parameters fields:', self.parameters)

        super().save(*args, **kwargs)


# 指令表
class Instruction(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name="指令名称")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
    code = models.CharField(max_length=10, verbose_name="指令代码")
    func = models.CharField(max_length=100, verbose_name="操作函数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="指令描述")

    def __str__(self):
        return str(self.name)

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
        return str(self.create_time)

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
        return str(self.create_time)

    class Meta:
        verbose_name = "设计备份"
        verbose_name_plural = "设计备份"
        ordering = ['id']


# ********************
# 作业进程设置
# ********************

# 监视事件表Event变更，变更事件后续作业时，同步变更事件指令表Event_instructions的内容
@receiver(m2m_changed, sender=Event.next.through)
def event_m2m_changed_handler(sender, instance, action, **kwargs):

    # 设定指令为 create_operation_proc
    instruction_create_operation_proc = Instruction.objects.get(name='create_operation_proc')

    # 获取后续作业
    next_operations = []
    if action == 'post_add':
        next_operations = instance.next.all()
        print('!!post_add:', next_operations)
    elif action == 'post_remove':
        next_operations = instance.next.all()
        print('##post_remove:', next_operations)
    
    # 删除原有事件指令
    Event_instructions.objects.filter(event=instance).delete()

    # 新增事件指令
    for operation in next_operations:
        Event_instructions.objects.create(
            event=instance,
            instruction=instruction_create_operation_proc,
            order=1,
            params=operation.name,    # 用后续作业name作为指令参数
        )


# 监视事件表变更，管理员删除事件表Event时，同步删除事件指令表Event_instructions的内容
@receiver(post_delete, sender=Event)
def event_post_delete_handler(sender, instance, **kwargs):
    Event_instructions.objects.filter(event=instance).delete()
