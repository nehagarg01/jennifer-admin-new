from __future__ import unicode_literals
from decimal import Decimal

from django.db import models

# Create your models here.
class ShippingSetting(models.Model):
    active = models.BooleanField(default=False)
    free_shipping = models.BooleanField(default=False)
    free_shipping_minimum = models.DecimalField(max_digits=14, decimal_places=2,
                                                default=Decimal('0.00'))
    shipping_max = models.DecimalField(max_digits=14, decimal_places=2,
                                       default=Decimal('0.00'))
