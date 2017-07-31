# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-30 21:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0011_auto_20170726_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curation',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
