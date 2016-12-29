# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-29 08:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20161229_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u7528\u6237\u90ae\u4ef6 id')),
                ('username', models.CharField(max_length=50, null=True)),
                ('email', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='email',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 29, 16, 56, 27, 12000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
