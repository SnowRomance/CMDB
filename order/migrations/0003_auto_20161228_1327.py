# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-28 05:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20161227_1501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='deal',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='email',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 28, 13, 27, 27, 448000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
