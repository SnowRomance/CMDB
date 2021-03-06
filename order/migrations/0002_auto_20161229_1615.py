# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-29 08:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='content',
            field=models.CharField(max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 29, 16, 15, 9, 188000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='email',
            name='from_user',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='email',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='to_user',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='\u90ae\u4ef6Id'),
        ),
    ]
