from rest_framework import serializers
from .models import *


class CharacterFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterField
        fields = '__all__'


class NumberFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberField
        fields = '__all__'


class DTFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTField
        fields = '__all__'


class ChoiceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceField
        fields = '__all__'


class RelatedFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedField
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = '__all__'


class BaseFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseForm
        fields = '__all__'


class OperandViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperandView
        fields = '__all__'