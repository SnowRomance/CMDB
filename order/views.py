#-*- coding:utf-8 -*-
from order.models import *
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import HTMLParser
import MySQLdb as mysql
from CMDB.settings_config import dbconfig, saltconfig
import cgi
import json

# Create your views here.

html_parser = HTMLParser.HTMLParser()

config_list = dbconfig()
db = mysql.connect(host=config_list["host"], user=config_list["user"] ,passwd=config_list["pass"], db=config_list["name"], charset="utf8")
db.autocommit(True)
c = db.cursor()

def inbox(request):
    user = request.user
    c.execute("select ae.*, aue.status from order_email ae, order_usermail aue where ae.id = aue.email_id and aue.status != 2")
    inbox_list = []
    for inbox_object in c.fetchall():
        inbox = {}
        inbox["id"] = inbox_object[0]
        inbox["from_user"] = inbox_object[3]
        inbox["to_user"] = inbox_object[5]
        inbox["title"] = inbox_object[4]
        inbox["content"] = inbox_object[1]
        inbox["create_time"] = inbox_object[2]
        inbox["status"] = inbox_object[6]
        print inbox["status"]
        inbox_list.append(inbox)
        print inbox_list
    return render_to_response("order/inbox.html", {"user": user, "inbox_list": inbox_list})


def outbox(request):
    user = request.user
    outbox_list = Email.objects.filter(from_user=user)
    return render_to_response("order/outbox.html", locals())


def change_status(request):
    id = request.POST.get("id")
    status = UserMail.objects.filter(email_id=id).update(status=1)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    rjson = json.dumps({"status": status})
    response.write(rjson)
    return response


def get_send_page(request):
    user = request.user
    email_title = request.GET.get("email_title")
    email_content = request.GET.get("email_content")
    email_from_user = request.GET.get("email_from_user")
    create_time = request.GET.get("create_time")
    return render_to_response("order/send.html", locals())


def send(request):
    from_user = request.user
    to_user = request.POST.get("to_user")
    title = request.POST.get("title")
    content = request.POST.get("content")
    print content
    email = Email()
    email.from_user = from_user
    email.to_user = to_user
    email.title = title
    email.content = content
    email.deal = 0
    email.save()

    user_mail = UserMail()
    user_mail.email_id = email.id
    user_mail.username = to_user
    user_mail.save()
    return HttpResponseRedirect("/order/outbox")
