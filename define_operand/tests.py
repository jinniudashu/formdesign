from django.test import TestCase

# Create your tests here.
for s in ss:
    if OperationsSetting.objects.filter(service = s).count() == 0:
        OperationsSetting.objects.create(service = s, operation = s.first_operation)
