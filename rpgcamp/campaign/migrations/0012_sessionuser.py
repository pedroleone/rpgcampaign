# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 21:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign', '0011_auto_20170416_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Não Informado'), (2, 'Não Vai Participar'), (3, 'Vai Participar'), (4, 'Não Sabe')], default=1)),
                ('note', models.CharField(max_length=100)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]