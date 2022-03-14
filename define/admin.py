from django.contrib import admin

from define.models import *

@admin.register(BoolField)
class BoolFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['name_icpc']

@admin.register(CharacterField)
class CharacterFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['name_icpc']

@admin.register(NumberField)
class NumberFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['name_icpc']

@admin.register(DTField)
class DTFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ["name_icpc", ]

@admin.register(RelatedField)
class RelatedFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['name_icpc']

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'label', 'content_type', 'object_id', 'hssc_id']
    search_fields=['label', 'pym']

@admin.register(ComponentsGroup)
class ComponentsGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']


@admin.register(DicDetail)
class DicDetailAdmin(admin.ModelAdmin):
    list_display = ('diclist', 'item', 'icpc')
    readonly_fields = ['hssc_id']
    autocomplete_fields = ['icpc', 'diclist']

class DicDetailInlineAdmin(admin.TabularInline):
    model = DicDetail
    exclude = ['name', 'label', 'hssc_id']
    autocomplete_fields = ['icpc', 'diclist']

@admin.register(DicList)
class DicListAdmin(admin.ModelAdmin):
    list_display = ('label', 'name')
    readonly_fields = ['name', 'related_field', 'hssc_id']
    search_fields=["pym"]
    inlines = [DicDetailInlineAdmin]

@admin.register(ManagedEntity)
class ManagedEntityAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'app_name', 'model_name', 'display_field', 'related_field']

# @admin.register(RelateFieldModel)
# class RelateFieldModelAdmin(admin.ModelAdmin):
#     readonly_fields = ['name', 'hssc_id']
