# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-25 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0008_auto_20170724_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='complink',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
