from import_export import resources
from define.models import Medicine

class MedicineResource(resources.ModelResource):
    class Meta:
        model = Medicine
        exclude = ['LastCycleDate']