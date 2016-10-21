import shopify
import datetime
from django.conf import settings

from .models import *
from vendors.models import Vendor


shop_url = "https://%s:%s@%s.myshopify.com/admin" % (
    settings.SHOPIFY_API_KEY,
    settings.SHOPIFY_PASSWORD,
    settings.SHOPIFY_SHOP_NAME,)

shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()


def sync_products():
    page = 1
    incomplete = True
    while incomplete:
        products = shopify.Product.find(page=page)
        if len(products):
            for sp in products:
                if sp.product_type not in ['living room sets', 'dining sets']:
                    product, created = Product.objects.update_or_create(
                        shopify_id=sp.id,
                        defaults={
                            'title': sp.title,
                            'body_html': sp.body_html,
                            'handle': sp.handle,
                            'product_type': ProductType.objects.get_or_create(title=sp.product_type)[0],
                            'published_at': sp.published_at,
                            'published_scope': sp.published_scope,
                            'vendor': Vendor.objects.get_or_create(name=sp.vendor)[0],
                        })
            page += 1
        else:
            incomplete = False
