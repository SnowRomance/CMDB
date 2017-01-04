# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.

class HostRequest(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'申请Id')
    username = models.CharField(max_length=50)
    hostname = models.CharField(max_length=30, default="", verbose_name=u'主机名')
    nick_name = models.CharField(max_length=30, null=True, verbose_name=u'主机别名')
    lease_time = models.IntegerField(default=30)  # 默认30天
    status = models.IntegerField(default=0)  # 0-未审批 1-通过 2-不通过
    create_time = models.DateField(default=datetime.datetime.now(), verbose_name=u'开始时间')

    def __unicode__(self):
        return {"id": self.id, "username": self.username, "hostname": self.hostname, "nick_name": self.nick_name,
                "lease_time": self.lease_time, "status": self.status, "create_time": str(self.create_time)}
