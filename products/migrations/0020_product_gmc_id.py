# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-04 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gmc_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
