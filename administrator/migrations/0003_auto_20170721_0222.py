# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-21 02:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_dataset_topic_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='curation',
            name='date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='data_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administrator.Dataset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='institute',
            field=models.CharField(default=1, max_length=140),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='curation',
            name='comment',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
