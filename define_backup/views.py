from django.shortcuts import render

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from define_operand.models import Project

class SourceCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceCode
        fields = '__all__'

@api_view(['GET'])
def source_codes_list(request,  **kwargs):
    print('Project:', kwargs['project_name'])
    project = Project.objects.get(name=kwargs['project_name'])
    source_codes = [SourceCode.objects.filter(project=project).last()]
    serializer = SourceCodeSerializer(source_codes, many=True)
    return Response(serializer.data)


class DesignBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignBackup
        fields = '__all__'

@api_view(['GET'])
def design_backup(request):
    design_backups = [DesignBackup.objects.last()]
    serializer = DesignBackupSerializer(design_backups, many=True)
    return Response(serializer.data)


class IcpcBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcpcBackup
        fields = '__all__'

@api_view(['GET'])
def get_icpc_backup(request):
    icpc_backup = [IcpcBackup.objects.last()]
    serializer = IcpcBackupSerializer(icpc_backup, many=True)
    return Response(serializer.data)