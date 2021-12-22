from django.shortcuts import render

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import SourceCode


class SourceCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceCode
        fields = '__all__'

@api_view(['GET'])
def source_codes_list(request):
    source_codes = SourceCode.objects.all()
    serializer = SourceCodeSerializer(source_codes, many=True)
    return Response(serializer.data)
