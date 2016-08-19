from __future__ import unicode_literals

from django.db import models
from localflavor.us.models import PhoneNumberField

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=128, unique=True)
    contact_person = models.CharField(max_length=128, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)

    def __unicode__(self):
        return self.name
