#-*- coding:utf-8 -*-
from order.models import *
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import HTMLParser
import cgi
import json

# Create your views here.

html_parser = HTMLParser.HTMLParser()

def inbox(request):
    user = request.user
    inbox_list = Email.objects.filter(~Q(status=2), to_user=request.user)
    return render_to_response("order/inbox.html", locals())


def outbox(request):
    user = request.user
    outbox_list = Email.objects.filter(~Q(status=2), from_user=request.user)
    return render_to_response("order/outbox.html", locals())


def change_status(request):
    id = request.POST.get("id")
    status = Email.objects.filter(id=id).update(status=1)
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
    return HttpResponseRedirect("/order/outbox")
