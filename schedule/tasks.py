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
    for schedule in Schedule.objects.filter(date=date).order_by('-schedule_type'):
        schedule.run_schedule()


@shared_task(bind=True)
def execute_change(self, variant_shopify_id, changes):
    try:
        variant = shopify.Variant.find(variant_shopify_id)
        variant.compare_at_price = float(changes['compare_at_price'])
        variant.price = float(changes['sale_price'] or changes['price'])
        # variant = shopify.Variant({
        #     'id': variant_shopify_id,
        #     'compare_at_price': float(changes['compare_at_price']),
        #     'price': float(changes['sale_price'] or changes['price']),
        # })
        result = variant.save()
        if result:
            Variant.objects.filter(id=changes['variant']).update(
                compare_at_price=changes['compare_at_price'],
                price=changes['price'], sale_price=changes['sale_price']
            )
            Schedule.update_status(changes['schedule'], result)
    except Exception as e:
        print e
        self.retry(exc=e, countdown=60)


@shared_task(bind=True)
def discount_product(self, product, schedule):
    try:

        s_product = shopify.Product({
            'id': product['shopify_id'],
            'variants': [],
        })
        variants = Variant.objects.filter(product_id=product['id'])
        discount = schedule['discount']
        discount = Decimal('1.00') - (Decimal(discount) / Decimal(100))
        for variant in variants:
            price = (variant.price * discount).quantize(
                Decimal('1.'), rounding=ROUND_UP) - Decimal('0.01')
            s_product.variants.append({
                'id': variant.shopify_id,
                'price': float(price)
            })
            variant.sale_price = price
            variant.save()
        result = s_product.save()
        if result:
            Schedule.update_status(schedule['id'], result)
    except Exception as e:
        self.retry(exc=e, countdown=60)

    # if s_product and 'EXCLUDE' not in s_product.tags:
    #     variants = Variant.objects.filter(product_id=product['id']).values('shopify_id', 'price')
    #     v_map = {}
    #     for d in variants:
    #         v_map[d['shopify_id']] = d['price']
    #     for v in s_product.variants:
    #         if 'clearance' in s_product.tags:
    #             discount = schedule['clearance_discount']
    #         else:
    #             discount = schedule['discount']
    #         discount = Decimal('1.00') - (Decimal(discount) / Decimal(100))
    #         price = (v_map[v.id] * discount).quantize(
    #             Decimal('1.'), rounding=ROUND_UP) - Decimal('0.01')
    #         v.price = float(price)
    #     result = s_product.save()
    #     Schedule.update_status(schedule['id'], result)


@shared_task(bind=True)
def restore_product(self, product, schedule_id=None):
    try:
        variants = Variant.objects.filter(product_id=product['id'])
        v_map = {}
        for d in variants.values('shopify_id', 'price'):
            v_map[d['shopify_id']] = float(d['price'])
        s_product = shopify.Product({
            'id': product['shopify_id'],
            'variants': v_map
        })
        result = s_product.save()
        if result and schedule_id:
            Schedule.update_status(schedule_id, result)
            variants.update(sale_price=Decimal('0.00'))
        return result
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True)
def update_theme(self, theme_id, schedule_id=None):
    try:
        theme = shopify.Theme({'id': theme_id, 'role': 'main'})
        result = theme.save()
        if result and schedule_id:
            Schedule.update_status(schedule_id, result)
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True)
def disable_discounts(self, schedule_id=None):
    try:
        discounts = shopify.Discount.find(page=1)
        for discount in discounts:
            if discount.status == 'enabled':
                discount.disable()
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task
def enable_discounts(codes):
    for code in codes.split(','):
        discount = shopify.Discount.find(code.strip())
        discount.enable()
