from __future__ import unicode_literals

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'

    def ready(self):
        import products.signals
