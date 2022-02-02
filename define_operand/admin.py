from django.contrib import admin

from .models import OperandView, SourceCode
from .utils import generate_source_code


class OperandViewAdmin(admin.ModelAdmin):
    readonly_fields = ['name']
    actions = [generate_source_code]


admin.site.register(OperandView, OperandViewAdmin)
admin.site.register(SourceCode)
