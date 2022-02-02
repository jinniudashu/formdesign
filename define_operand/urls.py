from django.urls import path
from .views import source_codes_list

urlpatterns = [
    path('source_codes_list/', source_codes_list, name='source_codes_list'),
]