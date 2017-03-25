from django.apps import AppConfig


class MnemotopyConfig(AppConfig):
    name = 'mnemotopy'
    verbose_name = 'Mnemotopy'

    def ready(self):
        super(MnemotopyConfig, self).ready()
