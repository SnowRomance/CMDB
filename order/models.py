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
    create_time = models.DateField(default=datetime.datetime.now(), verbose_name=u'创建时间')

    def __unicode__(self):
        return {"id": self.id, "from_user": self.from_user, "to_user": self.to_user, "title": self.title,
                "content": self.content, "create_time": self.create_time}


class UserMail(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u"用户邮件 id")
    username = models.CharField(null=True, max_length=50)
    email_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0) #0-未读 1-已读 2-删除

    def __unicode__(self):
        return {"id": self.id, "username": self.username, "email_id": self.email_id, "status": self.status}