# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-04 08:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20170104_1457'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HostRequest',
        ),
        migrations.AlterField(
            model_name='idc',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2017, 1, 4, 16, 28, 35, 853000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
