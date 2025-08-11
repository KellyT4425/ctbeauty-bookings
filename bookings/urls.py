from . import views
from django.urls import path
"""
URL configuration for the bookings app.

Defines routes for creating, listing, viewing detail, and cancelling bookings.
"""

app_name = 'bookings'

urlpatterns = [
    # path("home/", views.home, name="home"),
    # “/bookings/make/” — form to pick an available slot
    path("make/", views.make_booking, name="create"),

    # “/bookings/my/” — list of the current user’s bookings
    path("my/", views.my_bookings, name="list"),

    path('<int:pk>/', views.booking_detail, name='detail'),

    # “/bookings/cancel/42/” — cancel booking with pk=42
    path("cancel/<int:pk>/", views.cancel_booking, name="cancel"),
]
