from import_export import resources
from define.models import MedicineImport

class MedicineResource(resources.ModelResource):
    class Meta:
        model = MedicineImport
        exclude = ['LastCycleDate']