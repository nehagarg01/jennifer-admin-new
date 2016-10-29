import shopify
import datetime
from django.conf import settings

from .models import *
from vendors.models import Vendor


shopify.ShopifyResource.set_site(settings.SHOPIFY_URL)
# shop = shopify.Shop.current()


def sync_products():
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
