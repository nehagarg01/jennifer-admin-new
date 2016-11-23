import shopify
import datetime
from django.conf import settings

from vendors.models import Vendor

shopify.ShopifyResource.set_site(settings.SHOPIFY_URL)
# shop = shopify.Shop.current()


def pull_products():
    from .models import Product
    page = 1
    incomplete = True
    while incomplete:
        products = shopify.Product.find(page=page)
        if len(products):
            for sp in products:
                Product.update_from_shopify(sp)
            page += 1
        else:
            incomplete = False


def push_products(restore=False):
    from .tasks import push_product
    from .models import Product
    for product in Product.objects.all():
        push_product.delay(product.id, restore)
