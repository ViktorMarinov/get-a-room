# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 11:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='user_username',
            new_name='user_id',
        ),
    ]
