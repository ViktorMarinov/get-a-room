# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('capacity', models.PositiveIntegerField()),
                ('is_computer_room', models.BooleanField(default=False)),
            ],
        ),
    ]
