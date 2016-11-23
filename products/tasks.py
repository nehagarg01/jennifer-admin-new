from celery import shared_task

from .models import *
from .utils import shopify

@shared_task(rate_limit=3)
def sync_gmc_id(shopify_id):
    product = shopify.Product.find(shopify_id)
    metafields = product.metafields()
    for metafield in metafields:
        if metafield.attributes.get('key', None) == 'gmc_id':
            Product.objects.filter(shopify_id=shopify_id).update(
                gmc_id=metafield.attributes['value'])
            return True
    return 'No GMC_ID'


@shared_task(bind=True)
def push_product(self, product_id, restore=False):
    try:
        product = Product.objects.filter(id=product_id).first()
        if product:
            product.update_to_shopify(override=True, restore=restore)
    except Exception as e:
        self.retry(exc=e, countdown=60)
