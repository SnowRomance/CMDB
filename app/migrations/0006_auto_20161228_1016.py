# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-28 02:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20161228_1007'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='HostRequest',
        ),
        migrations.AlterField(
            model_name='idc',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 28, 10, 16, 27, 540000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]