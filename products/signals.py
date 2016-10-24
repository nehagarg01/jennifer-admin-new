from django.dispatch import receiver
from shopify_webhook.signals import products_update


@receiver(products_update)
def update_product(sender, data, **kwargs):
    from core.celery import add
    add.delay(1,2)
