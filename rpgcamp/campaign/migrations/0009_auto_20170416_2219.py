# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0008_campaignnotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignnotes',
            name='text',
            field=models.TextField(),
        ),
    ]
