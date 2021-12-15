import requests
import json
import time
from django.core.management import BaseCommand

# 写入文件
def write_to_file(file_name, content, mode='w'):
    output_path = '.\\define\\'   # views.py urls.py 导出路径
    with open(f'{output_path}{file_name}', mode, encoding='utf-8') as f:
        f.write(content)
    return      


class Command(BaseCommand):
    help = 'Import design from RMS and write to json file'

    # def add_arguments(self, parser):
    #     parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        # ***Create forms***
        url = 'https://hssc-rcms.herokuapp.com/forms'
        res = requests.get(url)
        res_json = res.json()
        print(res.status_code)
        write_to_file('rms_forms.json', json.dumps(res_json, indent=4, ensure_ascii=False))

        models = []
        for form in res_json:
            model_name = form['name'].replace(' ', '').lower()   # 表单名称
            model_label = form['label'].replace(' ', '')         # 显示名称
            model_style = form['style']                          # 表单样式: List/Detail
            if form['icpc_code']:
                model_icpc = form['icpc_code']['icpc_code']      # 是否为ICPC表单
            else:
                model_icpc = None
            
            fields = []
            for field in form['fields']:
                if field['name'] and field['label']:
                    # parse field, get a design sysytem format JSON
                    component = self._parse_field(field)
                    # append to model_components
                    # model_components.append(component)
                else:
                    component = 'Unknown field'
                    print('Unknown field')
                    
                fields.append(component)
            
            models.append({'name': model_name, 'label': model_label, 'style': model_style, 'icpc': model_icpc, 'fields': fields})
        
        write_to_file('design.json', json.dumps(models, indent=4, ensure_ascii=False))

    # parse field
    def _parse_field(self, field):
        name = field['name'].replace(' ', '').lower()
        label = field['label'].replace(' ', '')
        icpc_list = field['icpc_list']
        parameter = field['field_parameters']
        f_type = field['__component']
        if f_type == 'fields.char-field':
            input_style = field['input_style']
            auxiliary_input = field['auxiliary_input']
            score = field['score']
            # CharacterField
            if icpc_list is None and auxiliary_input is None:
                if parameter == 'CharField':
                    field_type = 'CharField'
                else:
                    field_type = 'TextField'
                # create field into CharacterField JSON
                return {'model': 'CharacterField', 'name': f'characterfield_{name}', 'label': label, 'type': field_type, 'score': score}

            # BoolField
            elif icpc_list is None and auxiliary_input is not None:
                if  auxiliary_input['id'] == 15:
                    # create field into BoolField JSON
                    return {'model': 'BoolField', 'name': f'boolfield_{name}', 'label': label, 'type': '0', 'score': score}
                elif auxiliary_input['id'] == 10:
                    # create field into BoolField JSON
                    return {'model': 'BoolField', 'name': f'boolfield_{name}', 'label': label, 'type': '1', 'score': score}
                else:
                    # create field into RelatedField JSON
                    type = self._get_input_style(input_style)
                    related_content = auxiliary_input['name'].replace(' ', '')
                    related_content_label = auxiliary_input['label'].replace(' ', '')
                    dic = self._get_dic(related_content)
                    return {'model': 'RelatedField', 'name': f'relatedfield_{name}', 'label': label, 'type': type, 'related_content': related_content, 'related_content_label': related_content_label, 'dic': dic, 'related_field': 'value', 'score': score}

            # RelatedField
            elif icpc_list is not None and auxiliary_input is None:
                # create field into RelatedField JSON
                type = self._get_input_style(input_style)
                related_content = icpc_list['name'].replace(' ', '')
                related_content_label = icpc_list['label'].replace(' ', '')
                dic = []
                return {'model': 'RelatedField', 'name': f'relatedfield_{name}', 'label': label, 'type': type, 'related_content': related_content, 'related_content_label': related_content_label, 'dic': dic, 'related_field': 'iname', 'score': score}
            
        elif f_type == 'fields.number-field':
            if parameter == 'SmallIntegerField' or parameter == 'PositiveSmallIntegerField':
                type = 'IntegerField'
            elif parameter == 'FloatField':
                type = 'FloatField'
            elif parameter == 'DecimalField':
                type = 'DecimalField'
            standard_value = field['standard']
            up_limit = field['up_limit']
            down_limit = field['down_limit']
            unit = field['unit']
            # create field into NumberField JSON
            return {'model': 'NumberField', 'name': f'numberfield_{name}', 'label': label, 'type': type, 'standard_value': standard_value, 'up_limit': up_limit, 'down_limit': down_limit, 'unit': unit}

        elif f_type == 'fields.date-field':
            if parameter == 'DateTimeField':
                type = 'DateTimeField'
            elif parameter == 'DateField':
                type = 'DateField'
            elif parameter == 'TimeField':
                type = 'TimeField'
            # create field into DTField JSON
            return {'model': 'DTField', 'name': f'datetimefield_{name}', 'label': label, 'type': type}
        else:
            return 'Unknown field'


    # [(Single_choice), (Dropdown_list), (Multi_choice), (Single_choice_input), (Multi_choice_input)]
    # CHOICE_TYPE = [('Select', '下拉单选'), ('RadioSelect', '单选按钮列表'), ('CheckboxSelectMultiple', '复选框列表'), ('SelectMultiple', '下拉多选')]
    def _get_input_style(self, input_style):
        if input_style == 'Single_choice':
            return 'RadioSelect'
        elif input_style == 'Dropdown_list':
            return 'Select'
        elif input_style == 'Multi_choice':
            return 'CheckboxSelectMultiple'
        elif input_style == 'Single_choice_input':
            return 'RadioSelect'
        elif input_style == 'Multi_choice_input':
            return 'CheckboxSelectMultiple'
        else:
            return 'Select'

    # 获取字典表
    def _get_dic(self, dic_name):
        dic = []
        url = f'https://hssc-rcms.herokuapp.com/dictionary-data?dictionary.name={dic_name}'
        res = requests.get(url)
        res_json = res.json()
        for item in res_json:
            dic.append(item['value'])
        print(dic)
        return dic
