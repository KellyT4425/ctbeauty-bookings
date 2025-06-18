from . import views
from django.urls import path

urlpatterns = [
    path('available-slots/', views.available_slots, name='available_slots'),

]
