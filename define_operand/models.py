from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, m2m_changed
import json
import uuid

from pypinyin import lazy_pinyin

from formdesign.hsscbase_class import HsscBase, HsscPymBase
from define.models import ManagedEntity, Component, ComponentsGroup, Role
from define_icpc.models import Icpc
from .utils import keyword_search
from define_backup.utils import GenerateModelsScriptMixin, GenerateViewsScriptMixin


# 业务表单定义
class BuessinessForm(GenerateModelsScriptMixin, HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    components = models.ManyToManyField(Component, blank=True, verbose_name="字段")
    components_groups = models.ManyToManyField(ComponentsGroup, blank=True, verbose_name="组件")
    managed_entities = models.ManyToManyField(ManagedEntity, through='FormEntityShip', verbose_name="关联实体")
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="表单说明")
    meta_data = models.JSONField(null=True, blank=True, verbose_name="元数据")
    script = models.TextField(blank=True, null=True, verbose_name='运行时脚本')
    
    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'

        # 生成meta_data
        if self.meta_data:
            meta_data = json.loads(self.meta_data)
        else:
            meta_data = {}
        meta_data['name'] = self.name
        meta_data['label'] = self.label
        meta_data['hssc_id'] = str(self.hssc_id)
        # 更新meta_data，类型为dict
        self.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name

    # 生成BuessinessForm的meta_data
    def generate_meta_data(self):
        meta_data = json.loads(self.meta_data)
        meta_data['fields'] = self.generate_components_meta_data(self.components.all())  # 根据components重新生成字段记录
        for components_group in self.components_groups.all():  # 根据components_groups重新生成字段记录
            meta_data['fields'].extend(self.generate_components_meta_data(components_group.components.all()))
        self.meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)

        # 生成models, admin, forms脚本
        self.script = json.dumps(self.generate_script(), ensure_ascii=False)
        self.save()

    # 生成BuessinessForm的字段的meta_data
    def generate_components_meta_data(self, components):
        fields = []
        for component in components:
            field = {}
            field['name'] = component.name
            field['label'] = component.label
            field['hssc_id'] = component.hssc_id
            _type = component.content_object._meta.object_name
            if _type == 'CharacterField':
                field['type'] = 'string'
            elif _type == 'NumberField':
                field['type'] = 'number'
            elif _type == 'DTField':
                field['type'] = 'datetime'
            elif _type == 'RelatedField':
                field['type'] = component.content_object.related_content.related_content  # 关联表的Model名称
                # 关联Model所属app名称，待补充!!!
                # related_content_type = component.content_object.related_content.related_content_type
                hssc_app_label = ''
                # if hssc_app_label == 'diclist':  # 字典表
                #     hssc_app_label = 'dictionaries'  # 指向hssc.dictionaries
                # elif hssc_app_label == 'managedentity':  # 实体表
                #     hssc_app_label = component.content_object.related_content.content_object.app_name  # 指向hssc.app_name
                field['app_label'] = hssc_app_label
            fields.append(field)
        return fields

# 重新生成字段的meta_data
@receiver(m2m_changed, sender=BuessinessForm.components.through)
def buessiness_form_components_changed_handler(sender, instance, action, reverse, model, pk_set, **kwargs):
    instance.generate_meta_data()

# 重新生成字段的meta_data
@receiver(m2m_changed, sender=BuessinessForm.components_groups.through)
def buessiness_form_components_groups_changed_handler(sender, instance, action, reverse, model, pk_set, **kwargs):
    instance.generate_meta_data()


# 表单和实体关系表
class FormEntityShip(HsscBase):
    entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, verbose_name="关联实体")
    form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="业务表单")
    is_base = models.BooleanField(default=False, verbose_name="基本信息表")

    def __str__(self):
        return str(self.entity) + '--' + str(self.form)

    class Meta:
        verbose_name = '表单和实体关系'
        verbose_name_plural = verbose_name


# # 系统作业指令表
class SystemOperand(HsscBase):
    func = models.CharField(max_length=255, blank=True, null=True, verbose_name="内部实现函数")
    parameters = models.CharField(max_length=255, blank=True, null=True, verbose_name="参数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    Applicable = [(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')]
    applicable = models.PositiveSmallIntegerField(choices=Applicable, default=1, verbose_name='适用范围')

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '系统自动作业'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 事件规则表
class EventRule(HsscBase):
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="表达式")
    Detection_scope = [(0, '所有历史表单'), (1, '本次服务表单'), (2, '单元服务表单')]
    detection_scope = models.PositiveSmallIntegerField(choices=Detection_scope, default=1, blank=True, null=True, verbose_name='检测范围')
    weight = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="权重")
    expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="内部表达式")

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '条件事件'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def generate_expression(self):  # 在EventRuleAdmin.save_formset中调用
        expressions = []
        descriptions = []
        for _expression in self.eventexpression_set.all():
            field = _expression.field  # 字段
            operator = EventExpression.Operator[_expression.operator][1]  # 操作符
            if ',' in _expression.value:
                value = f"[{_expression.value}]"  # 值为数组
            elif is_number(_expression.value):
                value = _expression.value  # 值为数字
            else:
                value = f"'{_expression.value}'"  # 值为字符串
            if _expression.connection_operator is not None and _expression.connection_operator >= 0:
                connection_operator = EventExpression.Connection_operator[_expression.connection_operator][1]  # 连接符
            else:
                connection_operator = ''
            expressions.extend([field.hssc_id, operator, value, connection_operator])
            descriptions.extend([field.label, operator, value, connection_operator])
        expressions.pop()   # 去掉最后一个连接符
        descriptions.pop()  # 去掉最后一个连接符
        self.expression = ' '.join(expressions)
        self.description = ' '.join(descriptions)
        self.save()
        return self.expression


# 事件表达式表
class EventExpression(HsscBase):
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE, null=True, blank=True, verbose_name="事件规则")
    field = models.ForeignKey(Component, on_delete=models.CASCADE, null=True, verbose_name="字段")
    Operator = [(0, '=='), (1, '!='), (2, '>'), (3, '<'), (4, '>='), (5, '<='), (6, 'in'), (7, 'not in')]
    operator = models.PositiveSmallIntegerField(choices=Operator, null=True, verbose_name='操作符')
    value = models.CharField(max_length=255, null=True, verbose_name="值", help_text="多个值用英文逗号分隔，空格会被忽略")
    Connection_operator = [(0, 'and'), (1, 'or')]
    connection_operator = models.PositiveSmallIntegerField(choices=Connection_operator, blank=True, null=True, verbose_name='连接操作符')

    def __str__(self):
        return str(self.event_rule.label)

    class Meta:
        verbose_name = '事件表达式'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 作业基础信息表
class Operation(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    buessiness_forms = models.ManyToManyField(BuessinessForm, through='BuessinessFormsSetting', verbose_name="作业表单")
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')
    Operation_priority = [
        (0, '0级'),
        (1, '紧急'),
        (2, '优先'),
        (3, '一般'),
    ]
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

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name
        ordering = ['id']


class BuessinessFormsSetting(HsscBase):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="作业")
    buessiness_form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    is_list = models.BooleanField(default=False, verbose_name="列表样式")

    def __str__(self):
        return str(self.buessiness_form)

    class Meta:
        verbose_name = '作业表单设置'
        verbose_name_plural = verbose_name
        ordering = ['id']


# # 单元服务类型信息表
class Service(GenerateViewsScriptMixin, HsscPymBase):
    name = models.CharField(max_length=255, unique=True, verbose_name="name")
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    label = models.CharField(max_length=255, verbose_name="名称")
    first_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='first_operation', null=True, verbose_name="起始作业")
    last_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='last_operation', blank=True, null=True, verbose_name="结束作业")
    # operations = models.ManyToManyField(Operation, through='OperationsSetting', verbose_name="包含作业")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, verbose_name="管理实体")
    Begin_time_setting = [(0, '人工指定时间'), (1, '引用出生日期')]
    begin_time_setting = models.PositiveSmallIntegerField(choices=Begin_time_setting, default=0, verbose_name='开始时间设置')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    group = models.ManyToManyField(Role, verbose_name="服务角色")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_recommanded_list = models.BooleanField(default=True, verbose_name='显示推荐作业')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列计数')
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
    script = models.TextField(blank=True, null=True, verbose_name='运行时脚本', help_text="script['views'] , script['urls'], script['templates']")

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'

        # 生成views, template, urls 脚本
        # if self.first_operation.buessiness_form:
        #     self.script = json.dumps(self.generate_script(), ensure_ascii=False)

        super().save(*args, **kwargs)
    

# 接收表单数据
Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]

class OperationsSetting(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='单元服务')
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='operation', null=True, verbose_name='作业')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, limit_choices_to=Q(applicable__in = [0, 3]), blank=True, null=True, verbose_name='系统作业')
    next_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, blank=True, null=True, related_name='next_operation', verbose_name='后续作业')
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0, verbose_name='接收表单')

    def __str__(self):
        return str(self.service) + '--' + str(self.operation)

    class Meta:
        verbose_name = '作业关系设置'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 服务包类型信息表
class ServicePackage(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    services = models.ManyToManyField(Service, through='ServicePackageDetail', verbose_name="服务项目")
    Begin_time_setting = [(0, '人工指定'), (1, '出生日期')]
    begin_time_setting = models.PositiveSmallIntegerField(choices=Begin_time_setting, default=0, verbose_name='开始时间参考')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "服务包"
        verbose_name_plural = verbose_name
        ordering = ['id']


class ServicePackageDetail(HsscPymBase):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    Cycle_options = [(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')]
    cycle_option = models.PositiveSmallIntegerField(choices=Cycle_options, default=0, blank=True, null=True, verbose_name='周期')
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="次数")
    reference_start_tim = models.DurationField(blank=True, null=True, verbose_name="参考起始时间", help_text='例如：3 days, 22:00:00')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    check_awaiting_timeout = models.BooleanField(default=False, verbose_name='检查等待超时')

    def __str__(self):
        return str(self.service)

    class Meta:
        verbose_name = "服务内容模板"
        verbose_name_plural = verbose_name
        ordering = ['id']



# 服务规格设置
class ServiceSpec(HsscBase):
    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "服务规则"
        verbose_name_plural = verbose_name
        ordering = ['id']


class ServiceProgramSetting(HsscBase):
    service_spec = models.ForeignKey(ServiceSpec, on_delete=models.CASCADE, null=True, verbose_name='服务规格')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE,  blank=True, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, limit_choices_to=Q(applicable__in = [1, 3]), blank=True, null=True, verbose_name='系统作业')
    next_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='next_service', verbose_name='后续服务')
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')
    Complete_feedback = [(0, '否'), (1, '返回完成状态'), (2, '返回表单')]
    complete_feedback = models.PositiveSmallIntegerField(choices=Complete_feedback, default=0,  blank=True, null=True, verbose_name='完成反馈')
    Reminders = [(0, '客户'), (1, '服务人员'), (2, '服务小组')]
    reminders = models.PositiveSmallIntegerField(choices=Reminders, default=0,  blank=True, null=True, verbose_name='提醒对象')
    message_content = models.CharField(max_length=255, blank=True, null=True, verbose_name='消息内容')
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    interval_rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔条件')
    interval_time = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')

    def __str__(self):
        return str(self.service)

    class Meta:
        verbose_name = '服务程序设置'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 判断传入的字符串是否是数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

#**********************************************************************************************************************
# 待清理代码，暂时保留供参考
#**********************************************************************************************************************

# 作业事件表
# # 默认事件：xx作业完成--系统作业名+"_operation_completed"
class Event(models.Model):
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="name")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='from_oid', verbose_name="所属作业")
    expression = models.TextField(max_length=1024, blank=True, null=True, default='completed', verbose_name="规则", 
        help_text='''
        说明：<br>
        1. 作业完成事件: completed<br>
        2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>
        3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"
        ''')
    next_operations = models.ManyToManyField(Operation, verbose_name="后续作业")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="事件描述")
    parameters = models.CharField(max_length=1024, blank=True, null=True, verbose_name="检查字段")
    fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="可用字段")
    event_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="作业事件ID")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = verbose_name
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

        if self.operation.form:
            form = json.loads(self.operation.form.meta_data)
            fields = []
            field_names = []
            form_name = form['name']
            for _field in form['fields']:
                field_name = form_name + '-' + _field['name']
                field_label = _field['label']
                field_type = _field['type']
                field_id = _field['hssc_id']
                field_names.append(field_name)
                fields.append(str((field_name, field_label, field_type, field_id)))

            self.fields = '\n'.join(fields)

            # 生成表达式参数列表
            if self.expression and self.expression != 'completed':
                _form_fields = keyword_search(self.expression, field_names)
                self.parameters = ', '.join(_form_fields)

        super().save(*args, **kwargs)


# 指令表
class Instruction(HsscBase):
    code = models.CharField(max_length=10, verbose_name="指令代码")
    func = models.CharField(max_length=100, verbose_name="操作函数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="指令描述")

    class Meta:
        verbose_name = "指令"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 作业事件指令程序表
class Event_instructions(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True, verbose_name="事件")
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, verbose_name="指令")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="指令序号")
    params = models.CharField(max_length=255, blank=True, null=True, verbose_name="创建作业")

    def __str__(self):
        return self.instruction.name

    class Meta:
        verbose_name = "作业事件指令集"
        verbose_name_plural = verbose_name
        ordering = ['event', 'order']


# ********************
# 作业进程设置
# ********************
# 监视事件路由表EventRoute变更，变更事件后续作业时，同步变更事件指令表Event_instructions的内容
# @receiver(post_save, sender=EventRoute)
# def event_route_post_save_handler(sender, instance, created, **kwargs):
#     if created:
#         # 设定指令为 create_operation_proc
#         instruction_create_operation_proc = Instruction.objects.get(name='create_operation_proc')
#         Event_instructions.objects.create(
#             event=instance.event,
#             instruction=instruction_create_operation_proc,
#             params=instance.operation.name,    # 用后续作业name作为指令参数
#         )

# @receiver(post_delete, sender=EventRoute)
# def event_route_post_delete_handler(sender, instance, **kwargs):
#     Event_instructions.objects.filter(event=instance.event, params=instance.operation.name).delete()
