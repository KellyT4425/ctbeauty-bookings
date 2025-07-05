from django.apps import AppConfig


# bookings/apps.py

from django.apps import AppConfig

class BookingsConfig(AppConfig):
    name = 'bookings'

    def ready(self):
        # Import signal handlers so they get registered
        import bookings.signals
