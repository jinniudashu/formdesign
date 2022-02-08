from django.urls import path
from .views import get_roles, get_operations, get_services, get_events, get_instructions, get_event_instructions, source_codes_list, design_backup

urlpatterns = [
    path('get_roles/', get_roles, name='get_roles'),
    path('get_operations/', get_operations, name='get_operations'),
    path('get_services/', get_services, name='get_services'),
    path('get_events/', get_events, name='get_events'),
    path('get_instructions/', get_instructions, name='get_instructions'),
    path('get_event_instructions/', get_event_instructions, name='get_event_instructions'),
    path('source_codes_list/', source_codes_list, name='source_codes_list'),
    path('design_backup/', design_backup, name='design_backup'),
]