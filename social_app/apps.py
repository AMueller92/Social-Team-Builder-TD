from django.apps import AppConfig


class SocialAppConfig(AppConfig):
    name = 'social_app'

    def ready(self):
        import social_app.signals
