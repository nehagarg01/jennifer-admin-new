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
                    for v in sp.variants:
                        variant, created = Variant.objects.update_or_create(
                            shopify_id=v.id, product=product,
                            defaults={
                                'sku': v.sku,
                                'barcode': v.barcode,
                                'compare_at_price': v.compare_at_price or 0,
                                'price': v.price or 0,
                                'pieces': v.grams,
                                'option1': v.option1,
                                'option2': v.option2,
                                'option3': v.option3,
                                'position': v.position,
                            })
                    attributes = []
                    for tag in sp.tags:
                        if 'style' in tag:
                            att, created = ProductAttribute.objects.get_or_create(
                                attribute_type='ST', title=tag.split('-')[1],
                                handle=tag
                            )
                            attributes.append(att)
                        elif 'material' in tag:
                            att, created = ProductAttribute.objects.get_or_create(
                                attribute_type='MA', title=tag.split('-')[1],
                                handle=tag
                            )
                            attributes.append(att)
                    product.attributes.add(*attributes)
            page += 1
        else:
            incomplete = False
