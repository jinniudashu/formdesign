from django.contrib import admin
from .models import DicList, DicDetail, ManagedEntity


def export_diclist_content_to_dicdetail(modeladmin, request, queryset):
    for obj in queryset:
        DicDetail.objects.filter(diclist=obj).delete()
        print('正在导出：', obj.label, obj.name)
        content = obj.content.split('\n')
        for item in content:
            if item:
                print(item)
                DicDetail.objects.create(diclist=obj, item=item)

    print('从DicList导出字典明细到DicDetail完成')

export_diclist_content_to_dicdetail.short_description = '从DicList导出字典明细到DicDetail'


class DicDetailInlineAdmin(admin.TabularInline):
    model = DicDetail
    autocomplete_fields = ['icpc', 'diclist']

class DicDetailAdmin(admin.ModelAdmin):
    list_display = ('diclist', 'item', 'icpc')
    autocomplete_fields = ['icpc', 'diclist']
admin.site.register(DicDetail, DicDetailAdmin)

class DicListAdmin(admin.ModelAdmin):
    list_display = ('label', 'name')
    readonly_fields = ['name', 'content']
    search_fields=["label", "pym"]
    inlines = [DicDetailInlineAdmin]
    actions = [export_diclist_content_to_dicdetail]
admin.site.register(DicList, DicListAdmin)

admin.site.register(ManagedEntity)

