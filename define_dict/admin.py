from django.contrib import admin
from .models import DicList, DicDetail, ManagedEntity


class DicDetailInlineAdmin(admin.TabularInline):
    model = DicDetail
    autocomplete_fields = ['icpc', 'diclist']

class DicDetailAdmin(admin.ModelAdmin):
    # model = DicDetail
    list_display = ('diclist', 'item', 'icpc')
    autocomplete_fields = ['icpc', 'diclist']
admin.site.register(DicDetail, DicDetailAdmin)

class DicListAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', )
    search_fields=["label", "pym"]
    inlines = [DicDetailInlineAdmin]
admin.site.register(DicList, DicListAdmin)

admin.site.register(ManagedEntity)

