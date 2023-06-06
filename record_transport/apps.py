from django.apps import AppConfig


class RecordTransportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "record_transport"

    # def ready(self):
    #     import record_transport.signals
