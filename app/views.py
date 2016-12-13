# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from app.models import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Create your views here.
def index(request):
    return render_to_response("index.html", {})

##### idc ###########
def idc(request):
    idc_list = Idc.objects.all()
    return render_to_response("idc.html", locals())


def get_add_idc_page(request):
    return render_to_response("add_idc.html", {})


def add_idc(request):
    idc_name = request.POST.get("idc_name")
    idc_remark = request.POST.get("idc_remark")
    print "In add"
    idc = Idc()
    idc.idc_name = str(idc_name)
    idc.remark = str(idc_remark)
    idc.save()
    return redirect("/app/idc/")
