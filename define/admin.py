from django.contrib import admin

from define.models import *

@admin.register(CharacterField)
class CharacterFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    search_fields=['label', 'pym']
    autocomplete_fields = ['name_icpc']

@admin.register(NumberField)
class NumberFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    search_fields=['label', 'pym']
    autocomplete_fields = ['name_icpc']

@admin.register(DTField)
class DTFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    search_fields=['label', 'pym']
    autocomplete_fields = ['name_icpc']

@admin.register(RelatedField)
class RelatedFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    search_fields=['label', 'pym']
    autocomplete_fields = ['name_icpc']

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'label', 'content_type', 'object_id', 'hssc_id']
    search_fields=['label', 'pym']

@admin.register(ComponentsGroup)
class ComponentsGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    search_fields=['label', 'pym']

# @admin.register(DicDetail)
# class DicDetailAdmin(admin.ModelAdmin):
#     list_display = ('diclist', 'item', 'icpc')
#     readonly_fields = ['hssc_id']
#     autocomplete_fields = ['icpc', 'diclist']

class DicDetailInlineAdmin(admin.TabularInline):
    model = DicDetail
    exclude = ['name', 'label', 'hssc_id', 'pym']
    autocomplete_fields = ['icpc']

@admin.register(DicList)
class DicListAdmin(admin.ModelAdmin):
    list_display = ('label', 'name')
    readonly_fields = ['name', 'hssc_id']
    search_fields=['label', 'pym']
    inlines = [DicDetailInlineAdmin]

@admin.register(ManagedEntity)
class ManagedEntityAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['label', 'id']
    list_display_links = ['label', ]
    search_fields = ['label', 'pym']
    readonly_fields = ['name', 'hssc_id']
    ordering = ['id']


# @admin.register(IcpcList)
# class IcpcListAdmin(admin.ModelAdmin):
#     readonly_fields = ['hssc_id', 'pym']

# @admin.register(RelateFieldModel)
# class RelateFieldModelAdmin(admin.ModelAdmin):
#     readonly_fields = ['name', 'hssc_id']
