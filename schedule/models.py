from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from django.forms.models import model_to_dict

from .tasks import execute_change, discount_product
from products.models import Product


class Schedule(models.Model):
    SCHEDULE_STATUS = (
        ('p', 'pending'),
        ('e', 'error'),
        ('c', 'completed'),
    )
    SCHEDULE_TYPE=(
        ('manual', 'manual'),
        ('storewide', 'storewide discount'),
        ('collection', 'collection discount'),
    )
    title = models.CharField(max_length=250)
    date = models.DateField()
    status = models.CharField(max_length=2, choices=SCHEDULE_STATUS, default='p')
    schedule_type = models.CharField(max_length=25, choices=SCHEDULE_TYPE,
                                     default='manual')
    discount = models.IntegerField(blank=True, null=True)
    clearance_discount = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def run_schedule(self):
        if self.schedule_type == 'manual':
            for change in self.changes.all():
                change.execute()
        elif self.schedule_type == 'storewide':
            for product in Product.main_products.all():
                discount_product.delay(
                    model_to_dict(product), model_to_dict(self))


class Change(models.Model):
    schedule = models.ForeignKey(Schedule, related_name="changes")
    variant = models.ForeignKey('products.Variant')
    compare_at_price = models.DecimalField(max_digits=14, decimal_places=2,
                                           default=Decimal('0.00'))
    price = models.DecimalField(max_digits=14, decimal_places=2,
                                default=Decimal('0.00'))
    sale_price = models.DecimalField(max_digits=14, decimal_places=2,
                                     default=Decimal('0.00'))

    def run(self):
        execute_change.delay(
            self.variant.shopify_id, model_to_dict(self))
