from django.forms import ModelForm, MultipleChoiceField
from .models import IcpcBase, HintFields

class HintFieldsForm(ModelForm):
    # 获取IcpcBase的所有字段名
    ICPC_FIELDS = [(field.verbose_name, field.verbose_name) for field in IcpcBase._meta.get_fields()]
    hint_fields = MultipleChoiceField(choices=ICPC_FIELDS, required=False)

    class Meta:
        model = HintFields
        fields = '__all__'
    
    def clean_hint_fields(self):
        # 将选中的字段名列表转换为逗号分隔的字符串
        hint_fields = self.cleaned_data.get('hint_fields')
        if hint_fields:
            return ','.join(hint_fields)
        return hint_fields
