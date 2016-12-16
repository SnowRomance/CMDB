# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from app.models import *
import MySQLdb as mysql
from CMDB.settings_config import dbconfig
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
        c.execute("Select count(ag.id) from app_group ag, app_hostlist ah, app_hostlist_group ahg where "
                  "ag.id = ahg.group_id and ahg.hostlist_id = ah.id and ah.idc_name =%s" ,[ idc["idc_name"]])
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
    print "In add"
    idc = Idc()
    idc.idc_name = str(idc_name)
    idc.remark = str(idc_remark)
    idc.save()
    return redirect("/app/idc/")
