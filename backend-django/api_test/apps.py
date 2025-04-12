from django.apps import AppConfig


class ApiTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_test'

    def ready(self):
        import api_test.signals  # Import the signals module