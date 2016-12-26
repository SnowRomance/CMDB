# -*- coding: utf-8 -*-
from django.db import models
import datetime


class Idc(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'机房Id')
    idc_name = models.CharField(max_length=40, unique=True, verbose_name=u'机房名称')
    remark = models.CharField(max_length=40, verbose_name=u'备注')
    salt_ip = models.GenericIPAddressField(null=True, verbose_name=u'管理机器IP')
    jumper_ip = models.GenericIPAddressField(null=True, verbose_name=u'跳板机IP')
    create_time = models.DateField(default=datetime.datetime.now(), verbose_name=u'创建时间')

    def __unicode__(self):
        return {"id": self.id, "idc_name": self.idc_name, "remark": self.remark, "salt_ip": str(self.salt_ip), "jumper_ip": str(self.jumper_ip),"create_time": self.create_time}

    class Meta:
        verbose_name = u'机房列表'
        verbose_name_plural = u'机房列表'


class Group(models.Model):
    group_name = models.CharField(max_length=50, unique=True, default='', verbose_name=u'组名')
    idc_name = models.CharField(max_length=40, null=True, blank=True, verbose_name=u'所属机房')
    remark = models.CharField(max_length=50, null=True, default='', verbose_name=u'描述')

    def __unicode__(self):
        return {"group_name": self.group_name, 'idc_name': self.idc_name, 'remark': self.remark}

    class Meta:
        verbose_name = u'主机组信息'
        verbose_name_plural = u'主机组信息管理'


class HostList(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'主机Id')
    ip = models.GenericIPAddressField(verbose_name=u'IP地址')
    hostname = models.CharField(max_length=30, unique=True, verbose_name=u'主机名')
    group_name = models.CharField(max_length=50, null=True, verbose_name=u'组名')
    nick_name = models.CharField(max_length=30, null=True, verbose_name=u'主机别名')
    idc_name = models.CharField(max_length=40, null=True, blank=True, verbose_name=u'所属机房')
    inner_ip = models.CharField(max_length=20, null=True, verbose_name=u'内网IP地址')

    def __unicode__(self):
        return {"id": self.id, "ip": self.ip, "hostname": self.hostname, "group_name": self.group_name, "nick_name": self.nick_name, "idc_name": self.idc_name, 'inner_ip': self.inner_ip}

    class Meta:
        verbose_name = u'主机列表'
        verbose_name_plural = u'主机列表'


class ServerAsset(models.Model):
    manufacturer = models.CharField(max_length=20, verbose_name=u'厂商')
    productname = models.CharField(max_length=30, verbose_name=u'产品型号')
    service_tag = models.CharField(max_length=80, unique=True, verbose_name=u'序列号')
    cpu_model = models.CharField(max_length=50, verbose_name=u'CPU型号')
    cpu_nums = models.PositiveSmallIntegerField(verbose_name=u'CPU线程数')
    cpu_groups = models.PositiveSmallIntegerField(verbose_name=u'CPU物理核数')
    mem = models.CharField(max_length=100, verbose_name=u'内存大小')
    disk = models.CharField(max_length=300, verbose_name=u'硬盘大小')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    hostname_nick = models.CharField(max_length=50, null=True, verbose_name=u'主机别名')
    ip = models.CharField(max_length=20, verbose_name=u'IP地址')
    os = models.CharField(max_length=20, verbose_name=u'操作系统')

    def __unicode__(self):
        return {"manufacturer": self.manufacturer, "productname": self.productname, "service_tag": self.service_tag, "cpu_model": self.cpu_model, "cpu_nums": self.cpu_nums,
                "cpu_groups": self.cpu_groups, "mem": self.mem, "disk": self.disk, "hostname": self.hostname, "ip": self.ip, "os": self.os}

    class Meta:
        verbose_name = u'主机资产信息'
        verbose_name_plural = u'主机资产信息管理'


class Upload(models.Model):
    headImg = models.FileField(upload_to='./upload/')

    def __unicode__(self):
        return {"headImg": self.headImg}

    class Meta:
        verbose_name = u'文件上传'
        verbose_name_plural = u'文件上传'


class cmd_run(models.Model):
    ip = models.GenericIPAddressField(verbose_name=u'IP地址')
    command = models.CharField(max_length=30, verbose_name=u'命令')
    track_mark = models.IntegerField()

    def __unicode__(self):
        return {"ip": self.ip, "command": self.command, "track_mark": self.track_mark}

    class Meta:
        verbose_name = u'命令管理'
        verbose_name_plural = u'命令管理'


class salt_return(models.Model):
    fun = models.CharField(max_length=50)
    jid = models.CharField(max_length=255)
    result = models.TextField()
    host = models.CharField(max_length=255)
    success = models.CharField(max_length=10)
    full_ret = models.TextField()

    def __unicode__(self):
        return {"fun": self.fun, "jid": self.jid, "result": self.result, "host": self.host, "success": self.success, "full_ret": self.full_ret}

    class Meta:
        verbose_name = u'命令返回结果'
        verbose_name_plural = u'命令返回结果'


