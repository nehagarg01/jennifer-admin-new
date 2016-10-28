from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from django.urls import reverse
from localflavor.us.models import PhoneNumberField
from django_extensions.db.models import TitleDescriptionModel

from .managers import *


class ProductType(models.Model):
    title = models.CharField(max_length=250)
    code = models.CharField(max_length=50, blank=True)

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
    product_type = models.ForeignKey(ProductType, related_name="products")
    published_at = models.DateTimeField(null = True)
    published_scope = models.CharField(max_length = 64, default = 'global')
    vendor = models.ForeignKey('vendors.Vendor')
    attributes = models.ManyToManyField(ProductAttribute)
    shopify_id = models.BigIntegerField(null=True, blank=True)
    series = models.ForeignKey('series.Series', null=True, blank=True,
                               related_name="products")

    objects = models.Manager()
    main_products = MainProductManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    def materials(self):
        return self.attributes.filter(attribute_type="MA")

    def styles(self):
        return self.attributes.filter(attribute_type="ST")

    def features(self):
        return self.attributes.filter(attribute_type="FT")

    @classmethod
    def shopify_sync(cls, shopify_product):
        from vendors.models import Vendor
        product, created = cls.objects.update_or_create(
            shopify_id=shopify_product.id,
            defaults={
                'title': shopify_product.title,
                'body_html': shopify_product.body_html,
                'handle': shopify_product.handle,
                'product_type': ProductType.objects.get_or_create(
                    title=shopify_product.product_type)[0],
                'published_at': shopify_product.published_at,
                'published_scope': shopify_product.published_scope,
                'vendor': Vendor.objects.get_or_create(name=shopify_product.vendor)[0],
            })
        for v in shopify_product.variants:
            variant, created = Variant.objects.update_or_create(
                shopify_id=v.id, product=product,
                defaults={
                    'sku': v.sku,
                    'barcode': v.barcode,
                    'compare_at_price': v.compare_at_price or 0,
                    # 'price': v.price or 0,
                    'pieces': v.grams,
                    'option1': v.option1,
                    'option2': v.option2,
                    'option3': v.option3,
                    'position': v.position,
                })
            if variant.sale_price:
                variant.sale_price = v.price
            else:
                variant.price = v.price
            variant.save()


        attributes = []
        for tag in shopify_product.tags:
            if 'style' in tag:
                att, created = ProductAttribute.objects.get_or_create(
                    attribute_type='ST', title=tag.split('-')[1],
                    handle=tag
                )
                attributes.append(att)
            elif 'material' in tag:
                att, created = ProductAttribute.objects.get_or_create(
                    attribute_type='MA', title=tag.split('-')[1],
                    handle=tag
                )
                attributes.append(att)
        product.attributes.add(*attributes)


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

    def __unicode__(self):
        output = self.option1
        if self.option2:
            output += " / %s" % self.option2
        if self.option3:
            output += " / %s" % self.option3
        return output


class Dimension(models.Model):
    product = models.ForeignKey(Product, related_name="dimensions")
    title = models.CharField(max_length=255, default="default")
    width = models.DecimalField(max_digits=12, decimal_places=2)
    depth = models.DecimalField(max_digits=12, decimal_places=2)
    height = models.DecimalField(max_digits=12, decimal_places=2)
