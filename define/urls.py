from django.urls import path
from .views import *

urlpatterns = [
    path('', apiview, name='apiview'),
    path('character_fields_list/', character_fields_list, name='character_fields_list'),
    path('number_fields_list/', number_fields_list, name='number_fields_list'),
    path('datetime_fields_list/', datetime_fields_list, name='datetime_fields_list'),
    path('choice_fields_list/', choice_fields_list, name='choice_fields_list'),
    path('related_fields_list/', related_fields_list, name='related_fields_list'),
    path('components_list/', components_list, name='components_list'),
    path('component_detail/<int:pk>', component_detail, name='component_detail'),
    path('base_models_list/', base_models_list, name='base_models_list'),
    path('base_forms_list/', base_forms_list, name='base_forms_list'),
    path('operand_views_list/', operand_views_list, name='operand_views_list'),
]