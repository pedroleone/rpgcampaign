# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0024_auto_20170429_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamereport',
            name='title',
        ),
        migrations.AddField(
            model_name='gamereport',
            name='initial',
            field=models.BooleanField(default=False),
        ),
    ]
