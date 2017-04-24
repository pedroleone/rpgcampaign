# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 18:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0018_auto_20170421_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('gm_only_text', models.TextField()),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField()),
                ('campaign', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
            ],
        ),
    ]
