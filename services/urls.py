from . import views
from django.urls import path

app_name = "services"

urlpatterns = [
    path('', views.services_list, name='list'),
]
