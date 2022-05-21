from import_export import resources
from define.models import Medcine

class MedcineResource(resources.ModelResource):
    class Meta:
        model = Medcine
        exclude = ['LastCycleDate']