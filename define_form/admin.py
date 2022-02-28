from django.contrib import admin

from .models import BaseModel, BaseForm, CombineForm

from time import time
import json


# 生成视图查询副本, 被define.admin调用
def copy_form(modeladmin, request, queryset):
    for obj in queryset:
        t = int(time())
        f = BaseForm.objects.create(
            name=f'{obj.name}_query_{t}',
            label=f'{obj.label}_查询视图_{t}',
            basemodel=obj.basemodel,
            is_inquiry=True,
            style=obj.style,
        )

        # 重构meta_data
        meta_data = json.loads(obj.meta_data)
        print('重构meta_data', type(meta_data), meta_data)
        meta_data['name'] = f.name
        meta_data['label'] = f.label
        meta_data['mutate_or_inquiry'] = 'inquiry'
        f.meta_data = json.dumps(meta_data, ensure_ascii=False)
        f.components.add(*obj.components.all())
        f.save()

copy_form.short_description = '生成查询视图副本'


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'basemodel_id']
    autocomplete_fields = ["name_icpc", ]

class BaseFormAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'basemodel', 'meta_data', 'baseform_id']
    actions = [copy_form]

class CombineFormAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'is_base', 'meta_data', 'combineform_id']
    autocomplete_fields = ["name_icpc", ]


admin.site.register(BaseModel, BaseModelAdmin)
admin.site.register(BaseForm, BaseFormAdmin)
admin.site.register(CombineForm, CombineFormAdmin)
