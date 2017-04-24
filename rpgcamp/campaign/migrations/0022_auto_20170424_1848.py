# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 21:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0021_auto_20170424_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True)),
                ('gm_only_text', models.TextField(blank=True)),
                ('linked_session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaign.Session')),
            ],
        ),
        migrations.AddField(
            model_name='campaignnotes',
            name='title',
            field=models.CharField(default='', max_length=150),
        ),
    ]
