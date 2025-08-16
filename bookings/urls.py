from . import views
from django.urls import path
"""
URL configuration for the bookings app.

Defines routes for creating, listing, viewing detail, and cancelling bookings.
"""

app_name = 'bookings'

urlpatterns = [
    path("make/", views.make_booking, name="create"),
    path("my/", views.my_bookings, name="list"),
    path("<int:pk>/", views.booking_detail, name="detail"),
    path("edit/<int:pk>/", views.edit_booking, name="edit"),
    path("cancel/<int:pk>/", views.cancel_booking, name="cancel"),
]
