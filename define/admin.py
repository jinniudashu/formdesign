from django.contrib import admin

from define.models import BoolField, CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component


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


admin.site.register(BoolField, BoolFieldAdmin)
admin.site.register(CharacterField, CharacterFieldAdmin)
admin.site.register(NumberField, NumberFieldAdmin)
admin.site.register(DTField, DTFieldAdmin)
admin.site.register(ChoiceField, ChoiceFieldAdmin)
admin.site.register(RelatedField, RelatedFieldAdmin)
admin.site.register(Component, ComponentAdmin)
