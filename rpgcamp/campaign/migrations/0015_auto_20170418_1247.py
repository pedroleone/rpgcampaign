# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0014_auto_20170417_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionuser',
            name='note',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]