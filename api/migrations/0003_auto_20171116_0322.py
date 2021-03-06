# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20171116_0236'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Number')),
                ('due_date', models.DateField(blank=True, default=None, null=True, verbose_name='Due date')),
                ('expiration_date', models.DateField(blank=True, default=None, null=True, verbose_name='Exp date')),
                ('cvv', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='CVV')),
                ('limit', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Limit')),
                ('avilable_amount', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Available amount')),
            ],
        ),
        migrations.DeleteModel(
            name='Greeting',
        ),
    ]
