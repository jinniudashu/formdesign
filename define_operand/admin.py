from django.contrib import admin

from .models import Service, Operation, Event, Instruction, Event_instructions, SourceCode, DesignBackup
from .utils import generate_source_code, design_backup


class EventInline(admin.TabularInline):
    model = Event
    extra = 0


class OperationAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        (None, {
            'fields': (('label', 'name'), ('forms', 'priority'), 'group',)
        }),
        ('作业管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    search_fields = ['name', 'label']
    inlines = [EventInline]
    ordering = ['id']
    readonly_fields = ['name']
    actions = [generate_source_code]


class EventAdmin(admin.ModelAdmin):
#     change_form_template = "core/templates/change_form.html"
    list_display = ['label', 'name', 'operation', 'id']
    list_display_links = ['label', 'name', 'operation',]
    search_fields = ['name', 'label']
    readonly_fields = ['parameters']
    ordering = ['id']


admin.site.register(Operation, OperationAdmin)
admin.site.register(Event, EventAdmin)


class Event_instructionsAdmin(admin.ModelAdmin):
    list_display = ['event', 'instruction', 'order', 'params', 'id']
    list_display_links = ['event', 'instruction', 'order', 'params']
    search_fields = ['event']
    ordering = ['id']


class InstructionAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'code', 'func', 'description', 'id']
    list_display_links = ['label', 'name', 'code', 'func']
    search_fields = ['name']
    ordering = ['id']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name', ]
    search_fields = ['name']
    ordering = ['id']


admin.site.register(Instruction, InstructionAdmin)
admin.site.register(Event_instructions, Event_instructionsAdmin)
admin.site.register(Service, ServiceAdmin)

admin.site.register(SourceCode)

class DesignBackupAdmin(admin.ModelAdmin):
    actions = [design_backup]
admin.site.register(DesignBackup, DesignBackupAdmin)
