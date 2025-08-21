from django.apps import AppConfig
from django.conf import settings

class CoreConfig(AppConfig):
    """
    Core app configuration.

    On startup, this ensures the Django 'Site' object (used by allauth for
    building links in emails, like password reset) is automatically updated
    with values from environment variables (SITE_DOMAIN and SITE_NAME).

    Means you don’t have to manually change the Site in /admin/sites
    when switching between local dev (127.0.0.1:8000) and production
    (Heroku or your live domain).
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Update the Sites framework on startup using env values.
        try:
            from django.contrib.sites.models import Site
            Site.objects.update_or_create(
                id=getattr(settings, "SITE_ID", 1),
                defaults={
                    "domain": getattr(settings, "SITE_DOMAIN", "127.0.0.1:8000"),
                    "name": getattr(settings, "SITE_NAME", "CT Beauty"),
                },
            )
        except Exception:
            # Ignore if DB isn't ready (e.g., during collectstatic/migrate)
            pass
