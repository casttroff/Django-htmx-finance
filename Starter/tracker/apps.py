from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracker"

    def ready(self):
        from .models import Order, OrderTranslationOptions
        from modeltranslation.translator import translator
        translator.register(Order, OrderTranslationOptions)
    