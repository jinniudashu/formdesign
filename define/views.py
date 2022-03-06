from django.shortcuts import render

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DicList


class DicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicList
        fields = '__all__'

@api_view(['GET'])
def dic_list(request):
    dic_lists = DicList.objects.filter(content__isnull=False)
    serializer = DicListSerializer(dic_lists, many=True)
    return Response(serializer.data)
