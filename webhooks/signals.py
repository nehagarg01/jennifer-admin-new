from django.dispatch import receiver

from bunch import bunchify

from shopify_webhook.signals import products_update
from products.utils import shopify
from products.models import Product


@receiver(products_update)
def update_product(sender, data, **kwargs):
    return Product.update_from_shopify(bunchify(data))
