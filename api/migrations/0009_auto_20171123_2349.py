# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20171123_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='number',
            field=models.CharField(blank=True, default=None, max_length=25, null=True, unique=True, verbose_name='Number'),
        ),
    ]
