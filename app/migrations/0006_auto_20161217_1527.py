# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-17 07:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20161217_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostlist',
            name='idc_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='\u6240\u5c5e\u673a\u623f'),
        ),
        migrations.AlterField(
            model_name='idc',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 17, 15, 26, 59, 844000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
