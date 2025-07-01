from . import views
from django.urls import path

app_name = 'bookings'

urlpatterns = [
    # “/bookings/make/” — form to pick an available slot
    path("make/", views.make_booking, name="make"),

    # “/bookings/my/” — list of the current user’s bookings
    path("my/", views.my_bookings, name="list"),

    # “/bookings/cancel/42/” — cancel booking with pk=42
    path("cancel/<int:pk>/", views.cancel_booking, name="cancel"),
]
