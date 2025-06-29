from . import views
from django.urls import path

app_name = 'bookings'

urlpatterns = [
    path('make/', views.home, name='make'),
]
