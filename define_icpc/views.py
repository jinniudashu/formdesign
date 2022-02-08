from django.shortcuts import render

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import IcpcBackup, Icpc1_register_logins, Icpc2_reservation_investigations, Icpc3_symptoms_and_problems, Icpc4_physical_examination_and_tests, Icpc5_evaluation_and_diagnoses, Icpc6_prescribe_medicines, Icpc7_treatments, Icpc8_other_health_interventions, Icpc9_referral_consultations, Icpc10_test_results_and_statistics

class Icpc1_register_loginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc1_register_logins
        fields = '__all__'

@api_view(['GET'])
def get_icpc1_register_logins(request):
    icpc1_register_logins = Icpc1_register_logins.objects.all()
    serializer = Icpc1_register_loginsSerializer(icpc1_register_logins, many=True)
    return Response(serializer.data)


class Icpc2_reservation_investigationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc2_reservation_investigations
        fields = '__all__'

@api_view(['GET'])
def get_icpc2_reservation_investigations(request):
    icpc2_reservation_investigations = Icpc2_reservation_investigations.objects.all()
    serializer = Icpc2_reservation_investigationsSerializer(icpc2_reservation_investigations, many=True)
    return Response(serializer.data)


class Icpc3_symptoms_and_problemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc3_symptoms_and_problems
        fields = '__all__'

@api_view(['GET'])
def get_icpc3_symptoms_and_problems(request):
    icpc3_symptoms_and_problems = Icpc3_symptoms_and_problems.objects.all()
    serializer = Icpc3_symptoms_and_problemsSerializer(icpc3_symptoms_and_problems, many=True)
    return Response(serializer.data)


class Icpc4_physical_examination_and_testsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc4_physical_examination_and_tests
        fields = '__all__'

@api_view(['GET'])
def get_icpc4_physical_examination_and_tests(request):
    icpc4_physical_examination_and_tests = Icpc4_physical_examination_and_tests.objects.all()
    serializer = Icpc4_physical_examination_and_testsSerializer(icpc4_physical_examination_and_tests, many=True)
    return Response(serializer.data)


class Icpc5_evaluation_and_diagnosesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc5_evaluation_and_diagnoses
        fields = '__all__'

@api_view(['GET'])
def get_icpc5_evaluation_and_diagnoses(request):
    icpc5_evaluation_and_diagnoses = Icpc5_evaluation_and_diagnoses.objects.all()
    serializer = Icpc5_evaluation_and_diagnosesSerializer(icpc5_evaluation_and_diagnoses, many=True)
    return Response(serializer.data)


class Icpc6_prescribe_medicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc6_prescribe_medicines
        fields = '__all__'

@api_view(['GET'])
def get_icpc6_prescribe_medicines(request):
    icpc6_prescribe_medicines = Icpc6_prescribe_medicines.objects.all()
    serializer = Icpc6_prescribe_medicinesSerializer(icpc6_prescribe_medicines, many=True)
    return Response(serializer.data)


class Icpc7_treatmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc7_treatments
        fields = '__all__'

@api_view(['GET'])
def get_icpc7_treatments(request):
    icpc7_treatments = Icpc7_treatments.objects.all()
    serializer = Icpc7_treatmentsSerializer(icpc7_treatments, many=True)
    return Response(serializer.data)


class Icpc8_other_health_interventionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc8_other_health_interventions
        fields = '__all__'

@api_view(['GET'])
def get_icpc8_other_health_interventions(request):
    icpc8_other_health_interventions = Icpc8_other_health_interventions.objects.all()
    serializer = Icpc8_other_health_interventionsSerializer(icpc8_other_health_interventions, many=True)
    return Response(serializer.data)


class Icpc9_referral_consultationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc9_referral_consultations
        fields = '__all__'

@api_view(['GET'])
def get_icpc9_referral_consultations(request):
    icpc9_referral_consultations = Icpc9_referral_consultations.objects.all()
    serializer = Icpc9_referral_consultationsSerializer(icpc9_referral_consultations, many=True)
    return Response(serializer.data)


class Icpc10_test_results_and_statisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc10_test_results_and_statistics
        fields = '__all__'

@api_view(['GET'])
def get_icpc10_test_results_and_statistics(request):
    icpc10_test_results_and_statistics = Icpc10_test_results_and_statistics.objects.all()
    serializer = Icpc10_test_results_and_statisticsSerializer(icpc10_test_results_and_statistics, many=True)
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