# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from app.models import *
import MySQLdb as mysql
from CMDB.settings_config import dbconfig
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

config_list = dbconfig()
db = mysql.connect(host=config_list["host"], user=config_list["user"] ,passwd=config_list["pass"], db=config_list["name"], charset="utf8")
db.autocommit(True)
c = db.cursor()


# Create your views here.
def index(request):
    return render_to_response("app/index.html", {})


##### idc ###########
def idc(request):
    idc_list = []
    idc_object_list = Idc.objects.all()
    for i in idc_object_list:
        idc = i.__unicode__()
        c.execute("Select count(ag.id) from app_group ag, app_idc ai where "
                  "ag.idc_name = %s", [idc["idc_name"]])
        idc["groups"] = c.fetchone()[0]
        c.execute("Select count(ah.id) from app_hostlist ah where ah.idc_name = %s", [idc["idc_name"]])
        idc["hosts"] = c.fetchone()[0]
        idc_list.append(idc)
    return render_to_response("app/idc.html", {"idc_list": idc_list})


def get_add_idc_page(request):
    return render_to_response("app/add_idc.html", {})


def add_idc(request):
    idc_name = request.POST.get("idc_name")
    idc_remark = request.POST.get("idc_remark")
    idc = Idc()
    idc.idc_name = str(idc_name)
    idc.remark = str(idc_remark)
    idc.save()
    return redirect("/app/idc/")


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
def group(request):
    group_list = []
    idc_object_list = Idc.objects.all()
    for i in idc_object_list:
        idc = i.__unicode__()
        c.execute("select ag.* from app_group ag, app_idc ai where ag.idc_name = %s", [idc["idc_name"]])
        for hg in c.fetchall():
            group = {}
            group["idc_remark"] = idc["remark"]
            group["group_id"] = hg[0]
            group["group_name"] = hg[1]
            group["remark"] = hg[3]
            group["host_count"] = HostList.objects.filter(group_name=hg[1]).count()
            group_list.append(group)
    return render_to_response("app/group.html", {"group_list": group_list})


def get_add_group_page(request):
    idc_list = Idc.objects.all()
    return render_to_response("app/add_group.html", locals())


def add_group(request):
    group_name = request.POST.get("group_name")
    idc_name = request.POST.get("idc_name")
    group = Group()
    group.group_name = str(group_name)
    group.idc_name = str(idc_name)
    group.save()
    return redirect("/app/group/")


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
def host_list(request):
    host_list = HostList.objects.all().order_by("idc_name", "group_name")
    return render_to_response("app/host_list.html", {"host_list": host_list})


def get_add_host_page(request):
    idc_list = Idc.objects.all()
    group_list = Group.objects.all()
    return render_to_response("app/add_host.html", {"idc_list": idc_list, "group_list": group_list})


def add_host(request):
    idc_name = request.POST.get("idc_name")
    group_name = request.POST.get("group_name")

