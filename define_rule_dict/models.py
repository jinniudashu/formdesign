from django.db import models
import uuid
from pypinyin import lazy_pinyin

from define.models import Component


# 事件规则表
class EventRule(models.Model):
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="name")
    expression = models.CharField(max_length=1024, blank=True, null=True, verbose_name="表达式")
    Detection_scope = [(0, '所有历史表单'), (1, '本次服务表单'), (2, '单元服务表单')]
    detection_scope = models.PositiveSmallIntegerField(choices=Detection_scope, default=1, blank=True, null=True, verbose_name='检测范围')
    weight = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="权重")
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="事件描述")
    event_rule_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="业务规则ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.event_rule_id is None:
            self.event_rule_id = uuid.uuid1()
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    def generate_expression(self):
        for expression in self.expression_set.all():
            print('expression:', expression.field, expression.operator, expression.value, expression.connection_operator)
        return self.expression

    class Meta:
        verbose_name = '事件规则'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 事件表达式表
class EventExpression(models.Model):
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE, null=True, blank=True, verbose_name="事件规则")
    field = models.ForeignKey(Component, on_delete=models.CASCADE, null=True, blank=True, verbose_name="字段")
    Operator = [(0, '等于'), (1, '不等于'), (2, '大于'), (3, '小于'), (4, '大于等于'), (5, '小于等于'), (6, '包含'), (7, '不包含'), (8, '在...里'), (9, '不在...里')]
    operator = models.PositiveSmallIntegerField(choices=Operator, blank=True, null=True, verbose_name='操作符')
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="值", help_text="多个值用英文逗号分隔")
    Connection_operator = [(0, '且'), (1, '或')]
    connection_operator = models.PositiveSmallIntegerField(choices=Connection_operator, blank=True, null=True, verbose_name='连接操作符')
    event_expression_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="事件表达式ID")

    def __str__(self):
        return str(self.event_rule.label)

    def save(self, *args, **kwargs):
        if self.event_expression_id is None:
            self.event_expression_id = uuid.uuid1()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '事件表达式'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 频度规则表
class FrequencyRule(models.Model):
    label = models.CharField(max_length=255, verbose_name="规则名称")
    name = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name="name")
    Cycle_options = [(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')]
    cycle_option = models.PositiveSmallIntegerField(choices=Cycle_options, default=0, blank=True, null=True, verbose_name='周期')
    times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="次数")
    frequency_rule_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="频度规则ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.frequency_rule_id is None:
            self.frequency_rule_id = uuid.uuid1()
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "频度规则"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 间隔规则表
class IntervalRule(models.Model):
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
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "间隔规则"
        verbose_name_plural = verbose_name
        ordering = ['id']