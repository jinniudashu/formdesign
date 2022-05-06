class GenerateModelsScriptMixin:
    # 生成models, admin, forms脚本
    def generate_script(self):
        script = {}
        script['models'], script['admin'] = self._create_model_script()
        return script

    # generate model and admin script
    def _create_model_script(self):
        # construct model script
        head_script = f'class {self.name.capitalize()}(HsscFormModel):'
        fields_script = autocomplete_fields = ''

        # !!!待修改：compontents = form.components.all() + form.component_groups.all()
        for component in self.components.all():
            # construct fields script
            _script = self._create_model_field_script(component)
            fields_script = fields_script + _script
            # construct admin autocomplete_fields script
            if component.content_object.__class__.__name__ == 'RelatedField':
                autocomplete_fields = autocomplete_fields + f'"{component.content_object.name}", '

        footer_script = self._create_model_footer_script()

        # construct model and admin script
        model_script = f'{head_script}{fields_script}{footer_script}\n\n'
        admin_script = self._create_admin_script(autocomplete_fields)
        return model_script, admin_script

    # generate admin script
    def _create_admin_script(self, autocomplete_fields):
        name = self.name.capitalize()
        if autocomplete_fields == '':
            _body = f'pass'
        else:
            _body = f'autocomplete_fields = [{autocomplete_fields}]'

        admin_script = f'''
class {name}Admin(admin.ModelAdmin):
    {_body}
admin.site.register({name}, {name}Admin)
'''
        return admin_script

    # generate model field script
    def _create_model_field_script(self, component):
        script = ''
        field = component.content_object.__dict__
        component_type = component.content_type.__dict__['model']
        if component_type == 'characterfield':
            script = self._create_char_field_script(field)
        elif component_type == 'numberfield':
            script = self._create_number_field_script(field)
        elif component_type == 'dtfield':
            script = self._create_datetime_field_script(field)
        elif component_type == 'relatedfield':
            field['foreign_key'] = component.content_object.related_content.related_content
            script = self._create_related_field_script(field)
        return script

    # 生成字符型字段定义脚本
    def _create_char_field_script(self, field):
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
    def _create_number_field_script(self, field):
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
    def _create_datetime_field_script(self, field):
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
    def _create_related_field_script(self, field):
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

    # generate model footer script
    def _create_model_footer_script(self):
        return f'''
    class Meta:
        verbose_name = '{self.label}'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('{self.name}_detail_url', kwargs={{'slug': self.slug}})

    def get_update_url(self):
        return reverse('{self.name}_update_url', kwargs={{'slug': self.slug}})
        '''


class GenerateServiceScriptMixin:
    # 生成运行时脚本的models, admin, views, urls, templates
    def generate_script(self):
        script = {}
        script['models'], script['admin'] = self._create_model_script()
        return script
    
    # generate model and admin script
    def _create_model_script(self):
        # construct model script
        head_script = f'class {self.name.capitalize()}(HsscFormModel):'

        # 添加表头字段
        fields_script, header_fields = self._construct_header_fields_script()

        # admin.py脚本设置
        fieldssets = f'("基本信息", {{"fields": (({header_fields}),)}}), '
        autocomplete_fields = ''

        for form in self.buessiness_forms.all():
        # !!!待修改：compontents = form.components.all() + form.component_groups.all()
            form_fields = ''
            for component in form.components.all():
                # construct fields script
                _script = self._create_model_field_script(component)
                fields_script = fields_script + _script
                # construct admin body fields script
                form_fields = form_fields + f'"{component.content_object.name}", '
                if component.content_object.__class__.__name__ == 'RelatedField':
                    autocomplete_fields = autocomplete_fields + f'"{component.content_object.name}", '
            # construct admin fieldset script
            fieldssets_set = f'\n        ("{form.label}", {{"fields": ({form_fields})}}), '
            fieldssets = fieldssets + fieldssets_set
        # construct admin script
        admin_script = self._create_admin_script(fieldssets, autocomplete_fields, header_fields)

        # construct model script
        footer_script = self._create_model_footer_script()
        model_script = f'{head_script}{fields_script}{footer_script}\n\n'

        return model_script, admin_script

    # generate admin script
    def _create_admin_script(self, fieldssets, autocomplete_fields, readonly_fields):
        name = self.name.capitalize()
        fieldssets = f'fieldsets = ({fieldssets})'
        readonly_fields = f'readonly_fields = [{readonly_fields}]'
        if autocomplete_fields:
            autocomplete_fields = f'autocomplete_fields = [{autocomplete_fields}]'

        admin_script = f'''
class {name}Admin(HsscFormAdmin):
    {fieldssets}
    {autocomplete_fields}
    {readonly_fields}
admin.site.register({name}, {name}Admin)
clinic_site.register({name}, {name}Admin)
'''
        return admin_script

    # 构建表头字段脚本
    def _construct_header_fields_script(self):
        fields_script = ''
        header_fields = ''
        for component in self.managed_entity.header_fields.all():
            # construct fields script
            _script = self._create_model_field_script(component)
            fields_script = fields_script + _script
            header_fields = header_fields + f'"{component.content_object.name}", '
        # 如果服务表单内包含基本信息表，返回空表头字段
        if self.managed_entity.base_form in self.buessiness_forms.all():
            header_fields = ''
        return fields_script, header_fields

    # generate model field script
    def _create_model_field_script(self, component):
        script = ''
        field = component.content_object.__dict__
        component_type = component.content_type.__dict__['model']
        if component_type == 'characterfield':
            script = self._create_char_field_script(field)
        elif component_type == 'numberfield':
            script = self._create_number_field_script(field)
        elif component_type == 'dtfield':
            script = self._create_datetime_field_script(field)
        elif component_type == 'relatedfield':
            field['foreign_key'] = component.content_object.related_content.related_content
            script = self._create_related_field_script(field)
        return script

    # 生成字符型字段定义脚本
    def _create_char_field_script(self, field):
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
    def _create_number_field_script(self, field):
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
    def _create_datetime_field_script(self, field):
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
    def _create_related_field_script(self, field):
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

    # generate model footer script
    def _create_model_footer_script(self):
        return f'''

    class Meta:
        verbose_name = '{self.label}'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        '''
