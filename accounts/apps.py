from django.apps import AppConfig


class SocialAppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import team_builder.accounts.signals
