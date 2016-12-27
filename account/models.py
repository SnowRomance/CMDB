# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'用户Id')
    user = models.OneToOneField(User, unique=True, verbose_name='用户')
    phone = models.CharField(max_length=20)
    permissions = models.IntegerField(default=0) #0-普通 1-运维 2-admin