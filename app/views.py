# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from app.models import *
import MySQLdb as mysql
from CMDB.settings_config import dbconfig, saltconfig
from django.contrib.auth.decorators import login_required
from app.backend.saltapi import SaltAPI
from django.contrib.auth.models import User
from account.models import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


config_list = dbconfig()
db = mysql.connect(host=config_list["host"], user=config_list["user"] ,passwd=config_list["pass"], db=config_list["name"], charset="utf8")
db.autocommit(True)
c = db.cursor()

config_list_sal = saltconfig()
sapi = SaltAPI(url=config_list_sal["salt_url"], username=config_list_sal["salt_user"], password=config_list_sal["salt_pass"])


# Create your views here.
@login_required
def index(request):
    return render_to_response("app/index.html", {'user': request.user})


##### idc ###########
@login_required
def idc(request):
    idc_list = []
    idc_object_list = Idc.objects.all()
    for i in idc_object_list:
        idc = i.__unicode__()
        c.execute("Select count(ag.id) from app_group ag where ag.idc_name = %s", [idc["idc_name"]])
        idc["groups"] = c.fetchone()[0]
        c.execute("Select count(ah.id) from app_hostlist ah where ah.idc_name = %s", [idc["idc_name"]])
        idc["hosts"] = c.fetchone()[0]
        idc_list.append(idc)
    return render_to_response("app/idc.html", {"user": request.user, "idc_list": idc_list})


@login_required
def get_add_idc_page(request):
    return render_to_response("app/add_idc.html", {"user": request.user})


@login_required
def add_idc(request):
    idc_name = request.POST.get("idc_name")
    idc_remark = request.POST.get("idc_remark")
    idc = Idc()
    idc.idc_name = str(idc_name)
    idc.remark = str(idc_remark)
    idc.save()
    return redirect("/app/idc/")


@login_required
def modify_idc_remark(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    idc_id = request.POST.get("idc_id")
    remark = request.POST.get("remark")
    fun = Idc.objects.filter(id=idc_id).update(remark=remark)
    rjson = json.dumps({"status": fun})
    response.write(rjson)
    return response


### group ###
@login_required
def group(request):
    group_list = []
    idc_object_list = Idc.objects.all()
    for i in idc_object_list:
        idc = i.__unicode__()
        c.execute("select ag.* from app_group ag where ag.idc_name = %s", [idc["idc_name"]])
        for hg in c.fetchall():
            group = {}
            group["idc_remark"] = idc["remark"]
            group["group_id"] = hg[0]
            group["group_name"] = hg[1]
            group["remark"] = hg[3]
            group["host_count"] = HostList.objects.filter(group_name=hg[1]).count()
            group_list.append(group)
    return render_to_response("app/group.html", {"user": request.user, "group_list": group_list})


@login_required
def get_add_group_page(request):
    user = request.user
    idc_list = Idc.objects.all()
    return render_to_response("app/add_group.html", locals())


@login_required
def add_group(request):
    group_name = request.POST.get("group_name")
    idc_name = request.POST.get("idc_name")
    group = Group()
    group.group_name = str(group_name)
    group.idc_name = str(idc_name)
    group.save()
    return redirect("/app/group/")


@login_required
def modify_group_remark(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    group_id = request.POST.get("group_id")
    remark = request.POST.get("remark")
    fun = Group.objects.filter(id=group_id).update(remark=remark)
    rjson = json.dumps({"status": fun})
    response.write(rjson)
    return response


### host_list ###
@login_required
def sync_host(request):
    accepet_keys = sapi.list_all_key()
    if accepet_keys:
        for ac_key in accepet_keys[0]:
            content = sapi.remote_noarg_execution(ac_key, 'grains.items')
            if len(content['ip_interfaces']) == 3:
                ip = content['ip_interfaces']['eth1'][0]
            else:
                ip = "N/A"
            host = HostList.objects.filter(hostname=ac_key, ip=ip)
            if not host:
                hostlist = HostList()
                hostlist.ip = ip
                hostlist.hostname = ac_key
                hostlist.nick_name = ac_key

                hostlist.idc_name = sapi.remote_execution(ac_key, 'cmd.run', {'arg1':'cat /tmp/cmdb.txt | grep "idc"'})[0][ac_key].split("=")[1]
                hostlist.group_name = sapi.remote_execution(ac_key, 'cmd.run', {'arg1':'cat /tmp/cmdb.txt | grep "group"'})[0][ac_key].split("=")[1]
                hostlist.inner_ip = content['ip_interfaces']['eth0'][0]
                hostlist.save()

    host_list = HostList.objects.all().order_by("idc_name", "group_name")
    response = HttpResponse()
    host_list_dict = {}
    inum = 0
    for host in host_list:
        host_list_dict[str(inum)] = host.__unicode__()
        inum += 1
    response['Content-Type'] = "text/javascript"
    rjson = json.dumps(host_list_dict)
    response.write(rjson)
    return response


@login_required
def host_list(request):
    user = request.user
    host_list = HostList.objects.all().order_by("idc_name", "group_name")
    return render_to_response("app/host_list.html", locals())


@login_required
def modify_host_nickname(request):
    host_id = request.POST.get("host_id")
    nickname = request.POST.get("nickname")
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    result = HostList.objects.filter(id=host_id).update(nick_name=nickname)
    rjson = json.dumps({"result": result})
    response.write(rjson)
    return response


@login_required
def modify_host_ip(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    host_id = request.POST.get("host_id")
    ip = request.POST.get("ip")
    result = HostList.objects.filter(id=host_id).update(ip=ip)
    rjson = json.dumps({"result": result})
    response.write(rjson)
    return response


@login_required
def modify_host_inner_ip(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    host_id = request.POST.get("host_id")
    inner_ip = request.POST.get("inner_ip")
    result = HostList.objects.filter(id=host_id).update(ip=inner_ip)
    rjson = json.dumps({"result": result})
    response.write(rjson)
    return response


@login_required
def get_add_host_page(request):
    idc_list = Idc.objects.all()
    group_list = Group.objects.all()
    salt_ip = config_list_sal["salt_ip"]
    return render_to_response("app/add_host.html", {"user": request.user, "salt_ip": salt_ip, "idc_list": idc_list, "group_list": group_list})

# def add_host(request):
#     install_string = "yum install epel-release -y;yum install salt-minion -y;sed -i 's/#master: salt/master: $1/g' /etc/salt/minion;service salt-minion start;"

