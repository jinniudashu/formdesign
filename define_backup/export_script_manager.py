from django.db import models
from django.forms.models import model_to_dict
import json

from .script_file_header import dict_models_head, dict_admin_head, dict_admin_content

# 自定义管理器：导出字典脚本，字典数据
class ExportDictManager(models.Manager):
    # 导出字典models.py, admin.py脚本
    def models_admin_script(self, fields=None):
        if self.model.__name__ != 'DicList':
            return 'Only DicList can use this function'
        else:
            models_script = dict_models_head
            admin_script = dict_admin_head            
            dicts = self.all()

            for dict in dicts:
                name = dict.name.capitalize()

                # 生成model脚本
                _model_script = f'''
class {name}(DictBase):
    class Meta:
        verbate_name = '{dict.label}'
        verbate_name_plural = verbate_name'''
                models_script = f'{models_script}\n\n{_model_script}'

                # 生成admin脚本
                _admin_script = f'''
@admin.register({name})
class {name}Admin(admin.ModelAdmin):{dict_admin_content}'''
                admin_script = f'{admin_script}\n\n{_admin_script}'

            return models_script, admin_script
    
    # 导出字典Json数据
    def dict_data(self, fields=None):
        if self.model.__name__ != 'DicDetail':
            return 'Only DicDetail can use this function'
        else:
            dict_data = []

            # 构造字典明细数据
            for item in self.all():
                item_dict = model_to_dict(item)
                item_dict['id'] = None
                if item_dict['icpc']:
                    item_dict['icpc'] = item.icpc.icpc_code
                item_dict['diclist'] = item.diclist.hssc_id
                dict_data.append(item_dict)

            return dict_data
