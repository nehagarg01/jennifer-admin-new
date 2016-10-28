from django.dispatch import receiver

from shopify_webhook.signals import products_create
from products.utils import shopify
from products.models import Product


@receiver(products_create)
def update_product(sender, data, **kwargs):
    Product.shopify_sync(data)
