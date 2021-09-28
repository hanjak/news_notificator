from django.apps import AppConfig


class News_updaterConfig(AppConfig):
    name = 'news_updater'

    def ready(self):
        from news_updater import updater
        updater.start()
