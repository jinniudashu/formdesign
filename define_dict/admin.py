from django.contrib import admin
from .models import DicList, DicDetail, ManagedEntity


class DicDetailInlineAdmin(admin.TabularInline):
    model = DicDetail
    autocomplete_fields = ['icpc', 'diclist']

class DicDetailAdmin(admin.ModelAdmin):
    list_display = ('diclist', 'item', 'icpc')
    readonly_fields = ['item_id']
    autocomplete_fields = ['icpc', 'diclist']
admin.site.register(DicDetail, DicDetailAdmin)

class DicListAdmin(admin.ModelAdmin):
    list_display = ('label', 'name')
    readonly_fields = ['name', 'related_field', 'dic_id']
    search_fields=["label", "pym"]
    inlines = [DicDetailInlineAdmin]
admin.site.register(DicList, DicListAdmin)

class ManagedEntityAdmin(admin.ModelAdmin):
    readonly_fields = ['entity_id']
admin.site.register(ManagedEntity, ManagedEntityAdmin)
