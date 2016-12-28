#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.


class Email(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'邮件Id')
    from_user = models.CharField(null=True, max_length=50)
    to_user = models.CharField(null=True, max_length=100)
    title = models.CharField(null=True, max_length=100)
    content = models.CharField(null=True, max_length=3000)
    status = models.IntegerField(default=0) #0-未读 1-已读 2-删除
    create_time = models.DateField(default=datetime.datetime.now(), verbose_name=u'创建时间')