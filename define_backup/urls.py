from django.urls import path
from .views import *

urlpatterns = [
    path('design_backup/', design_backup, name='design_backup'),
    path('get_icpc_backup/', get_icpc_backup, name='get_icpc_backup'),
    path('source_codes_list/<str:project_name>/', source_codes_list, name='source_codes_list'),
]