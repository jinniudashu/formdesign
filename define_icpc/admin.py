from django.contrib import admin

from .models import Icpc, Icpc1_register_logins, Icpc2_reservation_investigations, Icpc3_symptoms_and_problems, Icpc4_physical_examination_and_tests, Icpc5_evaluation_and_diagnoses, Icpc6_prescribe_medicines, Icpc7_treatments, Icpc8_other_health_interventions, Icpc9_referral_consultations, Icpc10_test_results_and_statistics


@admin.register(Icpc)
class IcpcAdmin(admin.ModelAdmin):
    list_display = ['icpc_code','icode','iname','iename','include','criteria','exclude','consider','icd10','icpc2','note','pym', 'subclass']
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = ['icpc_code','icode','iname','iename','include','criteria','exclude','consider','icd10','icpc2','note','pym', 'subclass']
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class SubIcpcAdmin(admin.ModelAdmin):
    list_display = ['icpc_code','icode','iname','iename','include','criteria','exclude','consider','icd10','icpc2','note','pym']
    search_fields=["iname", "pym", "icpc_code", "icode"]
    ordering = ["icpc_code"]

admin.site.register(Icpc1_register_logins, SubIcpcAdmin)

admin.site.register(Icpc2_reservation_investigations, SubIcpcAdmin)

admin.site.register(Icpc3_symptoms_and_problems, SubIcpcAdmin)

admin.site.register(Icpc4_physical_examination_and_tests, SubIcpcAdmin)

admin.site.register(Icpc5_evaluation_and_diagnoses, SubIcpcAdmin)

admin.site.register(Icpc6_prescribe_medicines, SubIcpcAdmin)

admin.site.register(Icpc7_treatments, SubIcpcAdmin)

admin.site.register(Icpc8_other_health_interventions, SubIcpcAdmin)

admin.site.register(Icpc9_referral_consultations, SubIcpcAdmin)

admin.site.register(Icpc10_test_results_and_statistics, SubIcpcAdmin)
