#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Email(models.Model):
    from_user = models.CharField(max_length=50)
    to_user = models.CharField(max_length=50)
    content = models.CharField(max_length=3000)
    deal = models.IntegerField() #0-未读 1-已读 2-删除