# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HTTPLoger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('httpStuff', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JWTRToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('JWTtoken', models.TextField(blank=True, null=True)),
            ],
        ),
    ]