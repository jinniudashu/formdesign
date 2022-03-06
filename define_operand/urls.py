from django.urls import path
from .views import get_roles, get_operations, get_service_packages, get_services, get_events, get_instructions, get_event_instructions

urlpatterns = [
    path('get_roles/', get_roles, name='get_roles'),
    path('get_operations/', get_operations, name='get_operations'),
    path('get_services/', get_services, name='get_services'),
    path('get_service_packages/', get_service_packages, name='get_service_packages'),
    path('get_events/', get_events, name='get_events'),
    path('get_instructions/', get_instructions, name='get_instructions'),
    path('get_event_instructions/', get_event_instructions, name='get_event_instructions'),
]