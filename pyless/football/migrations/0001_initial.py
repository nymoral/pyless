# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('closed', models.DateTimeField(blank=True, default=None, null=True)),
                ('ended', models.DateTimeField(blank=True, default=None, null=True)),
                ('result1', models.IntegerField(blank=True, null=True)),
                ('result2', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('short', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='football.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='football.Team'),
        ),
    ]