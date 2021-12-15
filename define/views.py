from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

@api_view(['GET'])
def apiview(request):
    api_urls = {
        'Components List': '/components_list/',
    }
    return Response(api_urls)


@api_view(['GET'])
def character_fields_list(request):
    character_fields = CharacterField.objects.all()
    serializer = CharacterFieldSerializer(character_fields, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def number_fields_list(request):
    number_fields = NumberField.objects.all()
    serializer = NumberFieldSerializer(number_fields, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def datetime_fields_list(request):
    datetime_fields = DTField.objects.all()
    serializer = DTFieldSerializer(datetime_fields, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def choice_fields_list(request):
    choice_fields = ChoiceField.objects.all()
    serializer = ChoiceFieldSerializer(choice_fields, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def related_fields_list(request):
    related_fields = RelatedField.objects.all()
    serializer = RelatedFieldSerializer(related_fields, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def components_list(request):
    components = Component.objects.all()
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def component_detail(request, pk):
    component = Component.objects.get(id=pk)
    serializer = ComponentSerializer(component, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def base_models_list(request):
    base_models = BaseModel.objects.all()
    serializer = BaseModelSerializer(base_models, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def base_forms_list(request):
    base_forms = BaseForm.objects.all()
    serializer = BaseFormSerializer(base_forms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def operand_views_list(request):
    operand_views = OperandView.objects.all()
    serializer = OperandViewSerializer(operand_views, many=True)
    return Response(serializer.data)