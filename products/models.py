from __future__ import unicode_literals

from django.db import models
from localflavor.us.models import PhoneNumberField
from django_extensions.db.models import TitleDescriptionModel


class ProductType(TitleDescriptionModel):
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
    body_html = models.TextField(verbose_name="Description")
    handle = models.CharField(max_length = 255, db_index = True)
    product_type = models.ForeignKey(ProductType)
    published_at = models.DateTimeField(null = True)
    published_scope = models.CharField(max_length = 64, default = 'global')
    template_suffix = models.CharField(max_length = 255, null = True)
    title = models.CharField(max_length = 255, db_index = True)
    vendor = models.ForeignKey('vendors.Vendor')
    attributes = models.ManyToManyField(ProductAttribute)

    def __unicode__(self):
        return self.title
