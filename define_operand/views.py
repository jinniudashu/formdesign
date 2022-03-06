from django.shortcuts import render

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Role, Operation, Service, ServicePackage, Event, Instruction, Event_instructions


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    # def to_representation(self, value):
    #     return value.label

@api_view(['GET'])
def get_roles(request):
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)


class OperationSerializer(serializers.ModelSerializer):
    meta_data = serializers.SerializerMethodField()
    group = RoleSerializer(read_only=True, many=True)

    class Meta:
        model = Operation
        fields = ('name', 'label', 'forms', 'priority', 'group', 'suppliers', 'not_suitable', 'time_limits', 'working_hours', 'frequency', 'cost', 'load_feedback', 'resource_materials', 'resource_devices', 'resource_knowledge', 'meta_data')
    
    def get_meta_data(self, obj):
        if obj.forms: meta_data = obj.forms.meta_data
        else: meta_data = None
        return meta_data

@api_view(['GET'])
def get_operations(request):
    operations = Operation.objects.all()
    serializer = OperationSerializer(operations, many=True)
    return Response(serializer.data)


class ServiceSerializer(serializers.ModelSerializer):
    first_operation = OperationSerializer(read_only=True)
    operations = OperationSerializer(read_only=True, many=True)
    class Meta:
        model = Service
        fields = ('name', 'label', 'first_operation', 'operations', 'priority', 'group', 'suppliers', 'not_suitable', 'time_limits', 'working_hours', 'frequency', 'cost', 'load_feedback', 'resource_materials', 'resource_devices', 'resource_knowledge')

@api_view(['GET'])
def get_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


class ServicePackageSerializer(serializers.ModelSerializer):
    first_service = ServiceSerializer(read_only=True)
    services = ServiceSerializer(read_only=True, many=True)
    class Meta:
        model = ServicePackage
        fields = ('name', 'label', 'first_service', 'services')

@api_view(['GET'])
def get_service_packages(request):
    service_packages = ServicePackage.objects.all()
    serializer = ServicePackageSerializer(service_packages, many=True)
    return Response(serializer.data)


class EventSerializer(serializers.ModelSerializer):
    operation = OperationSerializer(read_only=True)
    next_operations = OperationSerializer(read_only=True, many=True)
    class Meta:
        model = Event
        fields = '__all__'

@api_view(['GET'])
def get_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = '__all__'

@api_view(['GET'])
def get_instructions(request):
    instructions = Instruction.objects.all()
    serializer = InstructionSerializer(instructions, many=True)
    return Response(serializer.data)


class Event_instructionsSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    instruction = InstructionSerializer(read_only=True)
    class Meta:
        model = Event_instructions
        fields = '__all__'

@api_view(['GET'])
def get_event_instructions(request):
    event_instructions = Event_instructions.objects.all()
    serializer = Event_instructionsSerializer(event_instructions, many=True)
    return Response(serializer.data)