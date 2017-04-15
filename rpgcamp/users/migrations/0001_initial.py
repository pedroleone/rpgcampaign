# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 15:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', imagekit.models.fields.ProcessedImageField(upload_to='avatars')),
                ('display_name', models.CharField(max_length=50)),
                ('bio', models.CharField(max_length=1000)),
                ('facebook', models.URLField()),
                ('twitter', models.URLField()),
                ('home_city', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]