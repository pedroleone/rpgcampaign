# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 02:36
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0016_auto_20170420_1005'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='campaignuser',
            managers=[
                ('person', django.db.models.manager.Manager()),
            ],
        ),
    ]
