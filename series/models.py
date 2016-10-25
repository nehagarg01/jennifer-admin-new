from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

# Create your models here.
class Series(models.Model):
    title = models.CharField(max_length=250)
    vendor_title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50)
    vendor = models.ForeignKey('vendors.Vendor')
    shopify_id = models.BigIntegerField(blank=True, null=True)
    published_scope = models.CharField(max_length=250, default="global")

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('series-detail', kwargs={'pk': self.pk})
