from __future__ import absolute_import
from decimal import Decimal, ROUND_UP

from django.utils.timezone import now
from celery import shared_task

from products.utils import shopify
from products.models import Variant
from .models import *


@shared_task
def run_schedule():
    date = now().date()
    for schedule in Schedule.objects.filter(date=date):
        schedule.run_schedule()


@shared_task
def execute_change(variant_shopify_id, changes):
    variant = shopify.Variant.find(variant_shopify_id)
    if variant:
        variant.compare_at_price = float(changes['compare_at_price'])
        variant.price = float(changes['sale_price'] or changes['price'])
        result = variant.save()
        if result:
            v = Variant.objects.get(id=changes['variant'])
            v.compare_at_price = changes['compare_at_price']
            v.price = changes['price']
            v.sale_price = changes['sale_price']
            v.save()
            Schedule.update_status(changes['schedule'], result)


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
        result = s_product.save()
        Schedule.update_status(schedule['id'], result)


@shared_task(rate_limit=1)
def restore_product(product, schedule_id=None):
    try:
        s_product = shopify.Product.find(product['shopify_id'])
        if s_product:
            variants = Variant.objects.filter(
                product_id=product['id'])
            v_map = {}
            for d in variants.values('shopify_id', 'price'):
                v_map[d['shopify_id']] = d['price']
            for v in s_product.variants:
                v.price = float(v_map[v.id])
            result = s_product.save()
            if result and schedule_id:
                Schedule.update_status(schedule_id, result)
                variants.update(sale_price=Decimal('0.00'))
            return result
    except Exception as e:
        print e
        self.retry(exc=e, countdown=60)


@shared_task
def update_theme(theme_id, schedule_id=None):
    theme = shopify.Theme.find(theme_id)
    theme.role = 'main'
    result = theme.save()
    if result and schedule_id:
        Schedule.update_status(schedule_id, result)


@shared_task
def disable_discounts(schedule_id=None):
    discounts = shopify.Discount.find(page=1)
    for discount in discounts:
        discount.disable()


@shared_task
def enable_discounts(codes):
    for code in codes.split(','):
        discount = shopify.Discount.find(code.strip())
        discount.enable()
