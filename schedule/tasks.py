from __future__ import absolute_import
from decimal import Decimal, ROUND_UP

from django.utils.timezone import now
from celery import shared_task

from products.utils import shopify
from products.models import Variant


@shared_task
def run_schedule():
    from schedule.models import Schedule
    date = now().date()
    for schedule in Schedule.objects.filter(date=date):
        schedule.run_schedule()


@shared_task
def test_hello():
    print 'helo'
    from schedule.models import Schedule
    date = now().date()
    for schedule in Schedule.objects.filter(date=date):
        schedule.run_schedule()
        print 'hellooooo'


@shared_task
def execute_change(variant_shopify_id, changes):
    variant = shopify.Variant.find(variant_shopify_id)
    if variant:
        variant.compare_at_price = float(changes['compare_at_price'])
        variant.price = float(changes['sale_price'] or changes['price'])
        success = variant.save()
        if success:
            v = Variant.objects.get(id=changes['variant'])
            v.compare_at_price = changes['compare_at_price']
            v.price = changes['price']
            v.sale_price = changes['sale_price']
            v.save()
        return success
    return variant


@shared_task
def discount_product(product, schedule):
    s_product = shopify.Product.find(product['shopify_id'])
    if s_product and 'EXCLUDE' not in s_product.tags:
        variants = Variant.objects.filter(product_id=product['id']).values('shopify_id', 'price')
        v_map = {}
        for d in variants:
            v_map[d['shopify_id']] = d['price']
        for v in s_product.variants:
            if 'clearance' in s_product.tags:
                discount = schedule['clearance_discount']
            else:
                discount = schedule['discount']
            discount = Decimal('1.00') - (Decimal(discount) / Decimal(100))
            price = (v_map[v.id] * discount).quantize(
                Decimal('1.'), rounding=ROUND_UP) - Decimal('0.01')
            v.price = float(price)
        s_product.save()


@shared_task
def restore_product(product):
    s_product = shopify.Product.find(product['shopify_id'])
    if s_product:
        variants = Variant.objects.filter(product_id=product['id']).values('shopify_id', 'price')
        v_map = {}
        for d in variants:
            v_map[d['shopify_id']] = d['price']
        for v in s_product.variants:
            v.price = float(v_map[v.id])
        s_product.save()


@shared_task
def update_theme(theme_id):
    theme = shopify.Theme.find(theme_id)
    theme.role = 'main'
    theme.save()
