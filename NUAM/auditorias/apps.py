from django.apps import AppConfig


class AuditoriasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auditorias'

    def ready(self):
        import auditorias.signals  # noqa
