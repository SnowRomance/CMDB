# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-27 09:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20161227_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lease',
            name='hostList',
        ),
        migrations.AddField(
            model_name='lease',
            name='hostname',
            field=models.CharField(default=b'', max_length=30, unique=True, verbose_name='\u4e3b\u673a\u540d'),
        ),
        migrations.AlterField(
            model_name='idc',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 27, 17, 17, 12, 548000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
