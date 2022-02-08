from django.urls import path
from .views import dic_list

urlpatterns = [
    path('dic_list/', dic_list, name='dic_list'),
]