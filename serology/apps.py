from django.apps import AppConfig


class SerologyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serology'

    def ready(self):
        import serology.signals