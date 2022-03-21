from django.contrib import admin

from .models import EventRule, EventExpression, FrequencyRule, IntervalRule


class EventExpressionInline(admin.TabularInline):
    model = EventExpression
    exclude = ['label', 'name', 'hssc_id']
    autocomplete_fields = ['field']

@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'description', 'detection_scope', 'weight', 'id')
    list_display_links = ['label', 'name', 'description']
    search_fields=['label', 'name', 'pym']
    readonly_fields = ['expression', 'hssc_id']
    inlines = [EventExpressionInline]
    ordering = ('id',)

    # 生成表达式
    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        if instances:
            instances[0].event_rule.generate_expression()


# @admin.register(EventExpression)
# class EventExpressionAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['field']


@admin.register(FrequencyRule)
class FrequencyRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'cycle_option', 'times', 'id')
    list_display_links = ['label', 'cycle_option', 'times']
    readonly_fields = ['name', 'hssc_id']
    ordering = ('id',)


@admin.register(IntervalRule)
class IntervalRuldAdmin(admin.ModelAdmin):
    list_display = ['label', 'rule', 'interval', 'id']
    list_display_links = ['label', 'rule', 'interval']
    fieldsets = (
        (None, {
            'fields': ('label', ('rule', 'interval'), 'description', ('name', 'hssc_id'))
        }),
    )
    readonly_fields = ['name', 'hssc_id']
    ordering = ['id']