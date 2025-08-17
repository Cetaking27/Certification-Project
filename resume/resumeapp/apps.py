from django.apps import AppConfig


class ResumeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resumeapp'

    def ready(self):
        import resumeapp.signals