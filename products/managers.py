from django.db import models


class MainProductManager(models.Manager):
    def get_queryset(self):
        exclude = ['protection plans', 'Gift Card', 'DISCONTINUED']
        return super(MainProductManager, self).get_queryset().exclude(
            product_type__title__in=exclude)
