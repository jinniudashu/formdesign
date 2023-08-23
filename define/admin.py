from django.contrib import admin

from define.models import *

from import_export.admin import ImportExportModelAdmin
from define.resource import MedicineResource

class MedicineAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Medicine, MedicineAdmin)

class MedicineImportAdmin(ImportExportModelAdmin):
    resource_class = MedicineResource
admin.site.register(MedicineImport, MedicineImportAdmin)

@admin.register(CharacterField)
class CharacterFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym']
    search_fields=['label', 'pym']
    autocomplete_fields = ['name_icpc']

@admin.register(NumberField)
class NumberFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym']
    search_fields=['label', 'pym']
    autocomplete_fields = ['name_icpc']

@admin.register(DTField)
class DTFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym']
    search_fields=['label', 'pym']
    autocomplete_fields = ['name_icpc']

@admin.register(RelatedField)
class RelatedFieldAdmin(admin.ModelAdmin):
    list_display = ['label', 'name']
    readonly_fields = ['hssc_id', 'pym']
    search_fields=['label', 'pym', 'name']
    autocomplete_fields = ['name_icpc']

@admin.register(FileField)
class FileFieldAdmin(admin.ModelAdmin):
    list_display = ['label', 'name']
    readonly_fields = ['hssc_id', 'pym']
    search_fields=['label', 'pym', 'name']
    autocomplete_fields = ['name_icpc']

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['label', 'name']
    search_fields=['label', 'pym']
    readonly_fields = [field.name for field in Component._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

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

@admin.register(RelateFieldModel)
class RelateFieldModelAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'hssc_id']
