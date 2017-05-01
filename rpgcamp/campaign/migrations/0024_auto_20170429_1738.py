# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 20:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0023_gamereport_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamereport',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
