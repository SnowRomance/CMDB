# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-29 08:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20161229_1656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermail',
            old_name='email',
            new_name='email_id',
        ),
        migrations.AlterField(
            model_name='email',
            name='create_time',
            field=models.DateField(default=datetime.datetime(2016, 12, 29, 16, 58, 46, 8000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]