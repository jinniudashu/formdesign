from django.urls import path
from .views import source_codes_list, design_backup

urlpatterns = [
    path('source_codes_list/', source_codes_list, name='source_codes_list'),
    path('design_backup/', design_backup, name='design_backup'),
]