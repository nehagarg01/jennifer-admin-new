from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from localflavor.us.models import PhoneNumberField
from django_extensions.db.models import TitleDescriptionModel

from .managers import *


class ProductType(models.Model):
    title = models.CharField(max_length=250)
    def __unicode__(self):
         return self.title


class ProductAttribute(models.Model):
    ATTRIBUTE_TYPES = (
        ('MA', 'Material'),
        ('ST', 'Style'),
        ('FT', 'Feature'),
    )
    attribute_type = models.CharField(max_length=3, choices=ATTRIBUTE_TYPES)
    title = models.CharField(max_length=255)
    handle = models.CharField(max_length=255, help_text="shopify tag")

    def __unicode__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length = 255, db_index = True)
    body_html = models.TextField(verbose_name="Description")
    handle = models.CharField(max_length = 255)
    product_type = models.ForeignKey(ProductType)
    published_at = models.DateTimeField(null = True)
    published_scope = models.CharField(max_length = 64, default = 'global')
    vendor = models.ForeignKey('vendors.Vendor')
    attributes = models.ManyToManyField(ProductAttribute)
    shopify_id = models.BigIntegerField(null=True, blank=True)

    objects = models.Manager()
    main_products = MainProductManager()

    def __unicode__(self):
        return self.title

    def materials(self):
        return self.attributes.filter(attribute_type="MA")

    def styles(self):
        return self.attributes.filter(attribute_type="ST")

    def features(self):
        return self.attributes.filter(attribute_type="FT")


class Variant(models.Model):
    product = models.ForeignKey(Product, related_name='variants')
    sku = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    compare_at_price = models.DecimalField(max_digits=14, decimal_places=2,
                                           default=Decimal('0.00'))
    price = models.DecimalField(max_digits=14, decimal_places=2,
                                default=Decimal('0.00'))
    sale_price = models.DecimalField(max_digits=14, decimal_places=2,
                                     default=Decimal('0.00'))
    pieces = models.IntegerField(default=1)
    weight = models.DecimalField(max_digits=14, decimal_places=2,
                                 blank=True, null=True)
    option1 = models.CharField(max_length=255, default="Default Title")
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    shopify_id = models.BigIntegerField(null=True, blank=True)
    position = models.IntegerField(default=1)

    class Meta:
        ordering = ['position']


class Dimension(models.Model):
    product = models.ForeignKey(Product, related_name="dimensions")
    title = models.CharField(max_length=255, default="default")
    width = models.DecimalField(max_digits=12, decimal_places=2)
    depth = models.DecimalField(max_digits=12, decimal_places=2)
    height = models.DecimalField(max_digits=12, decimal_places=2)
