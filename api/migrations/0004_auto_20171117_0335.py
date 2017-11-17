# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 03:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20171116_0322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Owner name')),
            ],
        ),
        migrations.AddField(
            model_name='creditcard',
            name='wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Wallet'),
        ),
    ]