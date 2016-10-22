from __future__ import unicode_literals
from decimal import Decimal

from django.db import models

# Create your models here.
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

    def __unicode__(self):
        return self.title


class Change(models.Model):
    schedule = models.ForeignKey(Schedule, related_name="changes")
    variant = models.ForeignKey('products.Variant')
    compare_at_price = models.DecimalField(max_digits=14, decimal_places=2,
                                           default=Decimal('0.00'))
    price = models.DecimalField(max_digits=14, decimal_places=2,
                                default=Decimal('0.00'))
    sale_price = models.DecimalField(max_digits=14, decimal_places=2,
                                     default=Decimal('0.00'))
