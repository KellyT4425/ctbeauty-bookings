from django.apps import AppConfig

class BookingsConfig(AppConfig):
    """App config for the bookings app; wires signals on startup."""
    name = 'bookings'

    def ready(self):
        """Register model signal handlers."""
        # Import signal handlers so they get registered
        import bookings.signals
