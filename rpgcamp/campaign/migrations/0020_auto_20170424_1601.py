# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0019_houserules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houserules',
            name='gm_only_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='houserules',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]