from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from pypinyin import lazy_pinyin

from hsscbase_class import HsscBase
from define.models import Component


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


# 间隔规则表
class IntervalRule(HsscBase):
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔规则')
    interval = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="说明")

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "间隔规则"
        verbose_name_plural = verbose_name
        ordering = ['id']
