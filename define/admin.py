from django.contrib import admin
from time import time

from .models import DicList, BoolField, CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component
from .models import ManagedEntity, BaseModel, BaseForm, CombineForm, OperandView, SourceCode
# from .models import InquireForm, MutateForm, 
from .utils import generate_source_code, copy_form


class BoolFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class CharacterFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class NumberFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class DTFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class ChoiceFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class RelatedFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class ComponentAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'label', 'content_type', 'object_id']

class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class BaseFormAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'basemodel', 'meta_data']
    actions = [copy_form]

class CombineFormAdmin(admin.ModelAdmin):
    readonly_fields = ['is_base']

class OperandViewAdmin(admin.ModelAdmin):
    readonly_fields = ['name']
    actions = [generate_source_code]

admin.site.register(BoolField, BoolFieldAdmin)
admin.site.register(CharacterField, CharacterFieldAdmin)
admin.site.register(NumberField, NumberFieldAdmin)
admin.site.register(DTField, DTFieldAdmin)
admin.site.register(ChoiceField, ChoiceFieldAdmin)
admin.site.register(DicList)
admin.site.register(RelatedField, RelatedFieldAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(ManagedEntity)
admin.site.register(BaseModel, BaseModelAdmin)
admin.site.register(BaseForm, BaseFormAdmin)
admin.site.register(CombineForm, CombineFormAdmin)
admin.site.register(OperandView, OperandViewAdmin)
admin.site.register(SourceCode)
