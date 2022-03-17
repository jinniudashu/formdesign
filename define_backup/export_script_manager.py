from django.db import models
from django.forms.models import model_to_dict

from define_backup.files_head_setting import dict_models_head, dict_admin_head, dict_admin_content, models_file_head, admin_file_head, forms_file_head, form_footer

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


# 自定义管理器：导出models.py、admin.py脚本
class ExportBuessinessFormManager(models.Manager):
    # 导出业务表单models.py, admin.py脚本
    def models_admin_script(self, fields=None):
        if self.model.__name__ != 'BuessinessForm':
            return 'Only BuessinessForm can use this function'
        else:
            # construct models.py and admin.py script
            models_script = models_file_head
            admin_script =  admin_file_head
            for form in self.all():
                _s = self.__CreateModelScript(form)
                _m, _a = _s.create_script()
                models_script = models_script + _m
                admin_script = admin_script + _a

            return models_script, admin_script

    # 导出业务表单forms.py脚本
    def forms_script(self, fields=None):
        if self.model.__name__ != 'BuessinessForm':
            return 'Only BuessinessForm can use this function'
        else:
            # construct forms.py script
            forms_script = forms_file_head
            for form in self.all():
                _s = self.__CreateFormScript(form)
                _f = _s.create_script()
                forms_script = forms_script + _f

            return forms_script


    class __CreateModelScript:
        def __init__(self, form):
            self.name = form.name
            self.label = form.label
            # !!!待修改：compontents = form.components.all() + form.component_groups.all()
            self.components = form.components.all()

        # generate model and admin script
        def create_script(self):
            # construct model script
            head_script = f'class {self.name.capitalize()}(HsscBuessinessFormBase):'

            fields_script = autocomplete_fields = ''
            for component in self.components:
                # construct fields script
                script = self.__create_model_field_script(component)
                fields_script = fields_script + script
                # construct admin autocomplete_fields script
                if component.content_object.__class__.__name__ == 'RelatedField':
                    autocomplete_fields = autocomplete_fields + f'"{component.content_object.__dict__["name"]}", '

            footer_script = self.__create_model_footer_script()

            # construct model and admin script
            model_script = f'{head_script}{fields_script}{footer_script}\n\n'
            admin_script = self.__create_admin_script(autocomplete_fields)

            return model_script, admin_script

        # generate admin script
        def __create_admin_script(self, autocomplete_fields):
            name = self.name.capitalize()
            if autocomplete_fields != '':
                admin_script = f'''
@admin.register({name})
class {name}Admin(admin.ModelAdmin):
    autocomplete_fields = [{autocomplete_fields}]
    '''
            else:
                admin_script = f'''
admin.site.register({name})
    '''
            return admin_script

        # generate model field script
        def __create_model_field_script(self, component):
            script = ''
            field = component.content_object.__dict__
            component_type = component.content_type.__dict__['model']
            if component_type == 'characterfield':
                script = self.__create_char_field_script(field)
            elif component_type == 'numberfield':
                script = self.__create_number_field_script(field)
            elif component_type == 'dtfield':
                script = self.__create_datetime_field_script(field)
            elif component_type == 'relatedfield':
                field['foreign_key'] = component.content_object.related_content.related_content
                script = self.__create_related_field_script(field)
            return script

        # generate model footer script
        def __create_model_footer_script(self):
            return f'''
        class Meta:
            verbose_name = '{self.label}'
            verbose_name_plural = verbose_name

        def get_absolute_url(self):
            return reverse('{self.name}_detail_url', kwargs={{'slug': self.slug}})

        def get_update_url(self):
            return reverse('{self.name}_update_url', kwargs={{'slug': self.slug}})
            '''

        # 生成字符型字段定义脚本
        def __create_char_field_script(self, field):
            if field['type'] == 'CharField':
                f_type = 'CharField'
            else:
                f_type = 'TextField'

            if field['required']:
                f_required = ''
            else:
                f_required = 'null=True, blank=True, '
            f_required = 'null=True, blank=True, '

            if field['default']:
                f_default = f'default="{field["default"]}", '
            else:
                f_default = ''

            return f'''
        {field['name']} = models.{f_type}(max_length={field['length']}, {f_default}{f_required}verbose_name='{field['label']}')'''

        # 生成数字型字段定义脚本
        def __create_number_field_script(self, field):
            if field['type'] == 'IntegerField':
                f_type = 'IntegerField'
                f_dicimal = ''
            elif field['type'] == 'DecimalField':
                f_type = 'DecimalField'
                f_dicimal = f'max_digits={field["max_digits"]}, decimal_places={field["decimal_places"]}, '
            else:
                f_type = 'FloatField'
                f_dicimal = ''
            
            if field['standard_value']:
                f_standard_value = f'default={field["standard_value"]}, '
            else:
                f_standard_value = ''
            if field['up_limit']:
                f_up_limit = f'default={field["up_limit"]}, '
            else:
                f_up_limit = ''
            if field['down_limit']:
                f_down_limit = f'default={field["down_limit"]}, '
            else:
                f_down_limit = ''

            if field['default']:
                f_default = f'default={field["default"]}, '
            else:
                f_default = ''

            if field['required']:
                f_required = 'null=True, '
            else:
                f_required = 'null=True, blank=True, '
            f_required = 'null=True, blank=True, '

            return f'''
        {field['name']} = models.{f_type}({f_dicimal}{f_default}{f_required}verbose_name='{field['label']}')
        {field['name']}_standard_value = models.{f_type}({f_dicimal}{f_standard_value}{f_required}verbose_name='{field['label']}标准值')
        {field['name']}_up_limit = models.{f_type}({f_dicimal}{f_up_limit}{f_required}verbose_name='{field['label']}上限')
        {field['name']}_down_limit = models.{f_type}({f_dicimal}{f_down_limit}{f_required}verbose_name='{field['label']}下限')'''
        
        # 生成日期型字段定义脚本
        def __create_datetime_field_script(self, field):
            f_default = ''
            if field['type'] == 'DateTimeField':
                f_type = 'DateTimeField'
                if field['default_now']: f_default = 'default=timezone.now(), '
            else:
                f_type = 'DateField'
                if field['default_now']: f_default = 'default=date.today(), '
            
            if field['required']:
                f_required = 'null=True, '
            else:
                f_required = 'null=True, blank=True, '

            return f'''
        {field['name']} = models.{f_type}({f_default}{f_required}verbose_name='{field['label']}')'''

        # 生成关联型字段定义脚本
        def __create_related_field_script(self, field):
            if field['type'] in ['Select', 'RadioSelect']:
                if field['type'] == 'Select':
                    f_type = 'Select'
                else:
                    f_type = 'RadioSelect'
                f_required = 'null=True, blank=True, '

                return f'''
        {field['name']} = models.ForeignKey({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', on_delete=models.CASCADE, {f_required}verbose_name='{field['label']}')'''

            elif field['type'] in ['SelectMultiple', 'CheckboxSelectMultiple']:
                if field['type'] == 'SelectMultiple':
                    f_type = 'SelectMultiple'
                else:
                    f_type = 'CheckboxSelectMultiple'

                return f'''
        {field['name']} = models.ManyToManyField({field['foreign_key']}, related_name='{field['foreign_key'].lower()}_for_{field['name']}_{self.name}', verbose_name='{field['label']}')'''


    class __CreateFormScript:
        def __init__(self, form):
            self.name = form.name.capitalize()
            self.label = form.label
            self.model = form.basemodel.name.capitalize()
            self.style = form.style
            self.components = form.components.all()
            self.fields = ''
            self.widgets = ''

        def create_script(self):
            for component in self.components:
                field_name = component.content_object.__dict__['name']
                # get fields
                self.fields = self.fields + f'\'{field_name}\', '

                # get widgets
                if component.content_type.__dict__['model'] in ['choicefield', 'relatedfield']:
                    field_type = component.content_object.__dict__['type']
                    if field_type == 'Select':
                        self.type = 'Select'
                    elif field_type == 'RadioSelect':
                        self.type = 'RadioSelect'
                    elif field_type == 'CheckboxSelectMultiple':
                        self.type = 'CheckboxSelectMultiple'
                    else:
                        self.type = 'SelectMultiple'
                    self.widgets = self.widgets + f'\'{field_name}\': {self.type}, '

            if self.widgets != '':
                self.widgets = f'widgets = {{{self.widgets}}}'

            # construct forms script
            head_script = f'''
    class {self.name}_ModelForm(ModelForm):'''

            body_script = f'''
        class Meta:
            model = {self.model}
            fields = [{self.fields}]
            {self.widgets}
            '''

            return f'{head_script}{body_script}{form_footer}'
