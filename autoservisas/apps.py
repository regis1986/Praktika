from django.apps import AppConfig


class AutoservisasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoservisas'

    def ready(self):
        from .signals import create_profile
