#-*- coding:utf-8 -*-
from order.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

# Create your views here.


def inbox(request):
    inbox_list = Email.objects.filter(to_user=request.user)
    return render_to_response("order/inbox.html", {"inbox_list": inbox_list})


def outbox(request):
    outbox_list = Email.objects.filter(from_user=request.user)
    return render_to_response("order/outbox.html", {"outbox_list": outbox_list})


def send(request):
    from_user = request.user
    to_user = request.POST.get("to_user")
    content = request.POST.get("from_user")
    email = Email()
    email.from_user = from_user
    email.to_user = to_user
    email.content = content
    email.deal = 0
    email.save()
    return HttpResponseRedirect("order/outbox")
