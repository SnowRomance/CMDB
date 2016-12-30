# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-30 06:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20161230_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostrequest',
            name='nick_name',
            field=models.CharField(max_length=30, null=True, verbose_name='\u4e3b\u673a\u522b\u540d'),
        ),
        migrations.AlterField(
            model_name='hostrequest',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 30, 14, 4, 45, 984000), verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='idc',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 30, 14, 4, 45, 980000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
