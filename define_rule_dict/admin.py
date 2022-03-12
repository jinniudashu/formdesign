from django.contrib import admin

from .models import EventRule, EventExpression, FrequencyRule, IntervalRule


class EventExpressionInline(admin.TabularInline):
    model = EventExpression
    exclude = ['label', 'name', 'event_expression_id']

@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'description', 'detection_scope', 'weight', 'id')
    list_display_links = ['label', 'name', 'description']
    readonly_fields = ['expression', 'hssc_id']
    inlines = [EventExpressionInline]
    ordering = ('id',)


@admin.register(FrequencyRule)
class FrequencyRuleAdmin(admin.ModelAdmin):
    list_display = ('cycle_option', 'times', 'id')
    list_display_links = ['cycle_option', 'times']
    # readonly_fields = ['hssc_id']
    ordering = ('id',)


@admin.register(IntervalRule)
class IntervalRuldAdmin(admin.ModelAdmin):
    list_display = ['rule', 'interval', 'id']
    list_display_links = ['rule', 'interval']
    fieldsets = (
        (None, {
            'fields': ('label', ('rule', 'interval'), 'description', ('name', 'operand_interval_rule_id'))
        }),
    )
    # readonly_fields = ['hssc_id']
    ordering = ['id']