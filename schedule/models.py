from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from django.forms.models import model_to_dict
from django.contrib.postgres.fields import JSONField

from products.models import Product


class Schedule(models.Model):
    SCHEDULE_STATUS = (
        ('p', 'pending'),
        ('i', 'in progress'),
        ('e', 'error'),
        ('c', 'completed'),
    )
    SCHEDULE_TYPE=(
        ('manual', 'manual'),
        ('storewide', 'storewide discount'),
        ('collection', 'collection discount'),
        ('restore', 'restore'),
    )
    title = models.CharField(max_length=250)
    date = models.DateField()
    status = models.CharField(max_length=2, choices=SCHEDULE_STATUS, default='p')
    schedule_type = models.CharField(max_length=25, choices=SCHEDULE_TYPE,
                                     default='manual')
    discount = models.IntegerField(blank=True, null=True)
    clearance_discount = models.IntegerField(blank=True, null=True)
    exclude_promotion = models.BooleanField(default=False)
    theme = models.BigIntegerField(blank=True, null=True)
    coupons = models.CharField(max_length=250, default="None")
    task_total = models.IntegerField(default=0)
    task_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.title

    def run_schedule(self):
        from .tasks import (discount_product, restore_product, update_theme,
                            disable_discounts, execute_change)
        for change in self.changes.all():
            execute_change.delay(change.id)
        # self.status = 'i'
        # self.task_total = 1 if self.theme else 0
        # if self.schedule_type == 'manual':
        #     self.task_total += self.changes.count()
        #     self.save()
        #     for product in Product.objects.filter(variants__changes__schedule=self):
        #         execute_change.delay(product.id, self.id)
        #     # for change in self.changes.all():
        #     #     change.run()
        # elif self.schedule_type == 'storewide':
        #     self.task_total += Product.main_products.count()
        #     self.save()
        #     for product in Product.main_products.all():
        #         discount_product.delay(
        #             model_to_dict(product), model_to_dict(self))
        # elif self.schedule_type == 'restore':
        #     queryset = Product.main_products.all()
        #     self.task_total += queryset.count()
        #     self.save()
        #     for product in queryset:
        #         restore_product.delay(model_to_dict(product), self.id)
        if self.theme:
            update_theme.delay(self.theme, self.id)
        # if self.coupons == '':
        #     disable_discounts.delay()


    @classmethod
    def update_status(cls, schedule_id, result):
        schedule = cls.objects.get(id=schedule_id)
        if result:
            schedule.task_count += 1
            if schedule.task_count == schedule.task_total and schedule.status == 'i':
                schedule.status = 'c'
        else:
            schedule.status = 'e'
        schedule.save()


class Change(models.Model):
    schedule = models.ForeignKey(Schedule, related_name="changes")
    product = models.ForeignKey('products.Product', related_name="changes")
    json = JSONField()
    completed = models.BooleanField(default=False)

    def run(self):
        from .tasks import execute_change
        execute_change.delay(self.id)
