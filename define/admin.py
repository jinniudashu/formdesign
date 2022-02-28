from django.contrib import admin

from define.models import BoolField, CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component, RelateFieldModel

class BoolFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

class CharacterFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

class NumberFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

class DTFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

# class ChoiceFieldAdmin(admin.ModelAdmin):
#     readonly_fields = ['name', 'field_id']
    # autocomplete_fields = ["name_icpc", ]

class RelatedFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'field_id']
    autocomplete_fields = ["name_icpc", ]

class ComponentAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'label', 'content_type', 'object_id', 'field_id']

class RelateFieldModelAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'relate_field_model_id']

admin.site.register(BoolField, BoolFieldAdmin)
admin.site.register(CharacterField, CharacterFieldAdmin)
admin.site.register(NumberField, NumberFieldAdmin)
admin.site.register(DTField, DTFieldAdmin)
# admin.site.register(ChoiceField, ChoiceFieldAdmin)
admin.site.register(RelatedField, RelatedFieldAdmin)
admin.site.register(Component, ComponentAdmin)

admin.site.register(RelateFieldModel, RelateFieldModelAdmin)
