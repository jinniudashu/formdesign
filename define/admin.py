from django.contrib import admin

from define.models import BoolField, CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component, ComponentsGroup, RelateFieldModel

@admin.register(BoolField)
class BoolFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

@admin.register(CharacterField)
class CharacterFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

@admin.register(NumberField)
class NumberFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

@admin.register(DTField)
class DTFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

# @admin.register(ChoiceField)
# class ChoiceFieldAdmin(admin.ModelAdmin):
#     readonly_fields = ['name', 'field_id']
    # autocomplete_fields = ["name_icpc", ]

@admin.register(RelatedField)
class RelatedFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'label', 'content_type', 'object_id', 'field_id']

@admin.register(ComponentsGroup)
class ComponentsGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'components_group_id']

@admin.register(RelateFieldModel)
class RelateFieldModelAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'relate_field_model_id']
