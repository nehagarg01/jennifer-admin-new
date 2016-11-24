from __future__ import absolute_import
from decimal import Decimal, ROUND_UP
from copy import deepcopy

from django.utils.timezone import now
from celery import shared_task

from products.utils import shopify
from products.models import Variant, Product
from .models import *


@shared_task
def run_schedule():
    date = now().date()
    for schedule in Schedule.objects.filter(date=date).order_by('-schedule_type'):
        schedule.run_schedule()


# @shared_task(bind=True)
# def execute_change(self, variant_shopify_id, changes):
#     try:
#         variant = shopify.Variant.find(variant_shopify_id)
#         variant.compare_at_price = float(changes['compare_at_price'])
#         variant.price = float(changes['sale_price'] or changes['price'])
#         # variant = shopify.Variant({
#         #     'id': variant_shopify_id,
#         #     'compare_at_price': float(changes['compare_at_price']),
#         #     'price': float(changes['sale_price'] or changes['price']),
#         # })
#         result = variant.save()
#         if result:
#             Variant.objects.filter(id=changes['variant']).update(
#                 compare_at_price=changes['compare_at_price'],
#                 price=changes['price'], sale_price=changes['sale_price']
#             )
#             Schedule.update_status(changes['schedule'], result)
#     except Exception as e:
#         print e
#         self.retry(exc=e, countdown=60)


# @shared_task(bind=True)
# def execute_change(self, product_id, schedule_id):
#     try:
#         product = Product.objects.get(id=product_id)
#         changes = Change.objects.filter(variant__product=product,
#                                         schedule_id=schedule_id)
#         variants = []
#         for change in changes:
#             variants.append({
#                 'id': change.variant.shopify_id,
#                 'compare_at_price': float(change.compare_at_price),
#                 'price': float(change.sale_price or change.price),
#             })
#         s_product = shopify.Product({
#             'id': product.shopify_id,
#             'variants': variants,
#         })
#         result = s_product.save()
#         if result:
#             for change in changes:
#                 Variant.objects.filter(id=change.variant_id).update(
#                     compare_at_price=change.compare_at_price,
#                     price=change.price, sale_price=change.sale_price
#                 )
#             changes.update(completed=True)
#             Schedule.update_status(schedule_id, result)
#     except Exception as e:
#         self.retry(exc=e, countdown=60)


@shared_task(bind=True)
def execute_change(self, change_id):
    try:
        change = Change.objects.filter(id=change_id).first()
        if change:
            shopify_data = deepcopy(change.json)
            for v in shopify_data:
                v['id'] = v.pop('shopify_id')
                if v.get('sale_price', None):
                    v['price'] = v['sale_price']
            s_product = shopify.Product({
                'id': change.product.shopify_id,
                'variants': shopify_data,
            })
            result = s_product.save()
            if result:
                for variant in change.json:
                    Variant.objects.filter(shopify_id=variant['shopify_id']).update(
                        compare_at_price=variant['compare_at_price'],
                        price=variant['price'], sale_price=variant.get('sale_price', 0)
                    )
                change.completed = True
                change.save()
                Schedule.update_status(change.schedule_id, result)
            return result
    except Exception as e:
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
        v_map = []
        for v in variants:
            v_map.append({
                'id': v.shopify_id,
                'price': float(v.price),
            })
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


@shared_task(bind=True)
def generate_schedule_changes(self, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if schedule.schedule_type == 'storewide':
        products = Product.main_products.prefetch_related('variants')
        if schedule.exclude_promotion:
            products = products.exclude(tags__contains="CURRENT_SALE")
        if not schedule.clearance_discount:
            products = products.exclude(tags__contains="clearance")
        batch = []
        for product in products:
            discount = schedule.clearance_discount \
                if product.is_clearance() else schedule.discount
            discount = Decimal('1.00') - (Decimal(discount) / Decimal(100))
            variants = []
            for variant in product.variants.all():
                sale_price = (variant.price * discount).quantize(
                    Decimal('1.'), rounding=ROUND_UP) - Decimal('0.01')
                variants.append({
                    'shopify_id': variant.shopify_id,
                    'title': str(variant),
                    'sale_price': float(sale_price),
                    'price': float(variant.price),
                    'compare_at_price': float(variant.compare_at_price),
                })
            if len(variants):
                c = Change(schedule_id=schedule.id, product_id=product.id, json=variants)
                batch.append(c)
        Change.objects.bulk_create(batch)
    elif schedule.schedule_type == 'restore':
        products = Product.main_products.filter(
            variants__sale_price__gt=0).prefetch_related('variants').distinct()
        batch = []
        for product in products:
            variants = []
            for variant in product.variants.all():
                variants.append({
                    'shopify_id': variant.shopify_id,
                    'title': str(variant),
                    'price': float(variant.price),
                    'compare_at_price': float(variant.compare_at_price),
                })
            c = Change(schedule_id=schedule.id, product_id=product.id, json=list(variants))
            batch.append(c)
        Change.objects.bulk_create(batch)
    return True
