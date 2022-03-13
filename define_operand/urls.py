from django.urls import path
from .views import get_roles, get_operations, get_service_packages, get_services

urlpatterns = [
    path('get_roles/', get_roles, name='get_roles'),
    path('get_operations/', get_operations, name='get_operations'),
    path('get_services/', get_services, name='get_services'),
    path('get_service_packages/', get_service_packages, name='get_service_packages'),
]