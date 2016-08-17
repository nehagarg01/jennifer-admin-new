from __future__ import unicode_literals

from django.db import models
from localflavor.us.models import PhoneNumberField

# Create your models here.
class Vendor(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=128)
    contact_person = models.CharField(max_length=128)
    email = models.EmailField()
    phone = PhoneNumberField()

    def __unicode__(self):
        return self.name
