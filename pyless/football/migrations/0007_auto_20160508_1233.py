# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0006_auto_20160508_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='important',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='guess',
            name='result1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='guess',
            name='result2',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]