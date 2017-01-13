from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from django.urls import reverse
from localflavor.us.models import PhoneNumberField
from django_extensions.db.models import TitleDescriptionModel

from .managers import *
from .utils import shopify


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
    tags = models.TextField(blank=True)
    gmc_id = models.CharField(max_length=255, blank=True)

    objects = models.Manager()
    main_products = MainProductManager()

    class Meta:
        ordering = ['title']

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
    def update_from_shopify(cls, shopify_product):
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
                'tags': shopify_product.tags,
            })
        variants = []
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
            variants.append(v.id)
        product.variants.exclude(shopify_id__in=variants).delete()

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
        # Update metafields
        metafields = shopify_product.metafields()
        for metafield in metafields:
            if metafield.attributes.get('key', None) == 'gmc_id':
                product.gmc_id = metafield.attributes['value']
                product.save()
        return product

    def pull(self):
        from vendors.models import Vendor
        shopify_product = shopify.Product.find(self.shopify_id)
        if shopify_product:
            self.title = shopify_product.title
            self.body_html = shopify_product.body_html
            self.handle = shopify_product.handle
            self.product_type = ProductType.objects.get_or_create(
                title=shopify_product.product_type)[0]
            self.published_at = shopify_product.published_at
            self.published_scope = shopify_product.published_scope
            self.vendor = Vendor.objects.get_or_create(name=shopify_product.vendor)[0]
            self.tags = shopify_product.tags
            self.save()
            variants = []
            for v in shopify_product.variants:
                variant, created = Variant.objects.update_or_create(
                    shopify_id=v.id, product=self,
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
                variants.append(v.id)
            self.variants.exclude(shopify_id__in=variants).delete()
        else:
            return False

    def update_to_shopify(self, override=False, restore=False):
        product = shopify.Product({
            'id': self.shopify_id,
            'title': self.title,
            'body_html': self.body_html,
            'variants': [],
            'tags': self.tags,
            'product_type': self.product_type.title,
        })
        for variant in self.variants.all():
            obj = {
                'sku': variant.sku,
                'barcode': variant.barcode,
                'compare_at_price': float(variant.compare_at_price),
                'price': float(variant.sale_price or variant.price),
                'option1': variant.option1,
                'option2': variant.option2,
                'option3': variant.option3,
                'position': variant.position,
                'grams': variant.pieces,
                'image_id': variant.image_id,
            }
            if not override:
                obj['id'] = variant.id
            if restore:
                obj['price'] = float(variant.price)
            product.variants.append(obj)

        success = product.save()
        return success, product.errors

    def push_price(self, restore=False):
        product = shopify.Product({
            'id': self.shopify_id,
            'variants': [],
        })
        for variant in self.variants.all():
            obj = {
                'id': variant.id,
                'compare_at_price': float(variant.compare_at_price),
                'price': float(variant.sale_price or variant.price),
            }
            if restore:
                obj['price'] = float(variant.price)
            product.variants.append(obj)
        success = product.save()
        return success, product.errors

    def is_clearance(self):
        return 'clearance' in self.tags

    def discontinue(self):
        self.product_type = ProductType.objects.get(title="DISCONTINUED")
        if "DISCONTINUED" not in self.tags:
            self.tags += ", DISCONTINUED"
        self.save()
        product = shopify.Product({
            'id': self.shopify_id,
            'variants': [],
            'tags': self.tags,
            'product_type': self.product_type.title,
        })
        for variant in self.variants.all():
            obj = {
                'id': variant.shopify_id,
                "inventory_management" : "shopify",
                "inventory_quantity" : 0,
            }
            product.variants.append(obj)
        success = product.save()
        return success, product.errors



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
    mattress_pieces = models.IntegerField(default=0)
    image_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['product__title', 'position']

    def __unicode__(self):
        output = self.option1
        if self.option2:
            output += " / %s" % self.option2
        if self.option3:
            output += " / %s" % self.option3
        return output

    def get_product_group(self):
        free_delivery = 'FREE_DELIVERY' in self.product.tags
        non_delivery = self.product.product_type.title in [
            'protection plans', 'Gift Card']
        if free_delivery or non_delivery:
            return "free"
        elif self.product.product_type.title in ['sofas', 'chaises', 'sofa chaises',
                                       'loveseats', 'daybeds']:
            return 'upholstery'
        elif self.product.product_type.title == 'sectionals':
            return 'sectionals'
        elif self.product.product_type.title in ['living room sets', 'dining sets', 'bedroom sets']:
            price = self.sale_price or self.price
            if price < 1000:
                return 'set_lt_1000'
            elif price < 2000:
                return 'set_lt_2000'
            else:
                return 'set_gt_2000'
        elif self.product.product_type.title in ['sofa chairs', 'recliners', 'accent chairs']:
            return 'chairs'
        elif self.product.product_type.title == 'beds':
            return 'beds'
        elif self.product.product_type.title in ['mattresses', 'box springs']:
            return 'mattress_n_boxspring'
        else:
            return 'ancillary'


class Dimension(models.Model):
    product = models.ForeignKey(Product, related_name="dimensions")
    title = models.CharField(max_length=255, default="default")
    width = models.DecimalField(max_digits=12, decimal_places=2)
    depth = models.DecimalField(max_digits=12, decimal_places=2)
    height = models.DecimalField(max_digits=12, decimal_places=2)
