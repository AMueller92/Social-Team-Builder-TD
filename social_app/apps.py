from django.apps import AppConfig


class SocialAppConfig(AppConfig):
    name = 'social_app'

    def ready(self):
        import team_builder.social_app.signals
