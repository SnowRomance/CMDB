# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app.models import *
import MySQLdb as mysql
from CMDB.settings_config import dbconfig, saltconfig
from app.backend.saltapi import SaltAPI
from django.contrib.auth.models import User
from order.models import *
from account.models import *
import ConfigParser
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
def index(request):
    return render_to_response("app/index.html", {'user': request.user})


##### idc ###########
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


def get_add_idc_page(request):
    return render_to_response("app/add_idc.html", {"user": request.user})


def add_idc(request):
    idc_name = request.POST.get("idc_name")
    idc_remark = request.POST.get("idc_remark")
    idc_salt = request.POST.get("idc_salt")
    idc_jump = request.POST.get("idc_jump")
    idc = Idc()
    idc.idc_name = str(idc_name)
    idc.remark = str(idc_remark)
    idc.salt_ip = str(idc_salt)
    idc.jumper_ip = str(idc_jump)
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


def get_add_group_page(request):
    user = request.user
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
def sync_host(request):
    accepet_keys = sapi.list_all_key()
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

def modify_ip(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    id = request.POST.get("id")
    ip = request.POST.get("ip")
    result = c.execute("update app_hostlist ah set ip=%s where id=%s", [ip, id])
    rjson = json.dumps({"result": result})
    response.write(rjson)
    return response


def host_list(request):
    user = request.user
    host_list = HostList.objects.all().order_by("idc_name", "group_name")
    return render_to_response("app/host_list.html", locals())


def get_add_host_page(request):
    idc_list = Idc.objects.all()
    group_list = Group.objects.all()
    return render_to_response("app/add_host.html", {"user": request.user, "idc_list": idc_list, "group_list": group_list})

def add_host(request):
    install_string = "yum install epel-release -y;yum install salt-minion -y;sed -i 's/#master: salt/master: $1/g' /etc/salt/minion;service salt-minion start;"


#### user ###
def user_list(request):
    user = request.user
    user_list = UserProfile.objects.all()
    return render_to_response("app/user_list.html", locals())


def modify_user_permissions(request):
    user_id = request.POST.get("user_id")
    permissions = request.POST.get("permissions")
    result = UserProfile.objects.filter(id=user_id).update(permissions=permissions)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    rjson = json.dumps({"result": result})
    response.write(rjson)
    return response


#### approval ####
def change_idc(request):
    idc_name = request.POST.get("idc_name")
    group_list = Group.objects.filter(idc_name=idc_name)
    group_list_dict = {}
    inum = 0
    for group in group_list:
        group_list_dict[str(inum)] = group.__unicode__()
        inum += 1

    group_name = ""
    if len(group_list) != 0:
        group_name  = group_list[0].group_name
    host_list = HostList.objects.filter(group_name=group_name)
    host_list_dict = {}
    inum = 0
    for host in host_list:
        host_list_dict[str(inum)] = host.__unicode__()
        inum += 1

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    rjson = json.dumps({"group_list_dict": group_list_dict, "host_list_dict": host_list_dict})
    response.write(rjson)
    return response


def change_group(request):
    group_name = request.POST.get("group_name")
    host_list = HostList.objects.filter(group_name=group_name)
    host_list_dict = {}
    inum = 0
    for host in host_list:
        host_list_dict[str(inum)] = host.__unicode__()
        inum += 1
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    rjson = json.dumps(host_list_dict)
    response.write(rjson)
    return response


def get_host_dict(filterhost):
    host = {}

    host["id"] = filterhost[0]
    host["ip"] = filterhost[1]
    host["hostname"] = filterhost[2]
    host["group_name"] = filterhost[3]
    host["nick_name"] = filterhost[4]
    host["idc_name"] = filterhost[5]
    host["inner_ip"] = filterhost[6]

    return host


def get_approval_request(request):
    idc_list = Idc.objects.all()
    idc_name = idc_list[0].idc_name
    group_list = Group.objects.filter(idc_name=idc_name)
    group_name = group_list[0].group_name
    c.execute("select ah.* from app_hostlist ah where ah.hostname not in (select al.hostname from app_lease al) and ah.group_name='" + str(group_name) + "' and ah.idc_name='" + str(idc_name) + "'")

    host_list = []
    for filterhost in c.fetchall():
        host = get_host_dict(filterhost)
        host_list.append(host)
    return render_to_response("app/approval_request.html", {"user": request.user, "idc_list": idc_list, "group_list": group_list, "host_list": host_list})


def get_user_dict(filteruser):
    user = {}
    user["id"] = filteruser[0]
    user["password"] = filteruser[1]
    user["username"] = filteruser[4]
    user["email"] = filteruser[7]
    return user


def send_mail(from_user, to_user, title, content):
    email = Email()
    email.from_user = from_user
    email.to_user = to_user
    email.title = title
    email.content = content
    email.save()

    user_mail = UserMail()
    user_mail.email_id = email.id
    user_mail.username = to_user
    user_mail.save()

def approval_request(request):
    host_list = request.POST.get("host_list")
    host_list = json.loads(host_list)
    ### 获取 auth_user 的 email
    username = request.user
    hostname_list = []
    ### 插入申请请求
    for host in host_list:
        hostname = host["hostname"]
        nickname = host["nickname"]
        if not HostRequest.objects.filter(hostname=hostname):
            host_request = HostRequest()
            host_request.hostname = hostname
            host_request.username = username
            host_request.nickname = nickname
            host_request.save()
        hostname_list.append(nickname)

    c.execute("select auth_user.* from auth_user where username='" + str(username) + "'")
    filteruser = c.fetchone()
    if filteruser is not None:
        user = get_user_dict(filteruser)
        email = user["email"]
        ### 获取 user
        user = ""
        user_part = email.split('@')[0]
        for user_p in user_part.split('.'):
            user = user + user_p

        #### usermod -e 2010-09-28 test
        #### 发送邮件
        from_user = "admin"
        to_users_list = UserProfile.objects.filter(permissions=2)
        for to_user in to_users_list:
            content = user + "申请访问主机" + str(hostname_list)
            send_mail(from_user, to_user.user.username, "主机申请", content)

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    rjson = json.dumps({"status": True})
    response.write(rjson)
    return response


def get_approval_accept_page(request):
    user = request.user
    request_user_list = []
    c.execute("select distinct(ahq.username) from app_hostrequest ahq")
    for request_user in c.fetchall():
        request_user_list.append(request_user[0])

    host_requests = HostRequest.objects.filter(status=0, username=request_user_list[0])
    return render_to_response("app/approval_deal.html", locals())


def approval_accept(request):
    requestid_list = request.GET.get("requestid_list")
    request_status = request.GET.get("request_status")
    request_user = request.GET.get("request_user")
    request_nick_name_list = []
    requestid_list = requestid_list.split(",")
    print requestid_list
    for key in range(0, len(requestid_list)-1):
        host_request = HostRequest.objects.filter(id=requestid_list[key])
        request_nick_name_list.append(host_request[0].nick_name)
        hostname = host_request[0].hostname
        host = HostList.objects.filter(hostname=hostname)
        idc = Idc.objects.filter(idc_name=host[0].idc_name)
        salt_ip = idc[0].salt_ip
        jumper_ip = idc[0].jumper_ip
        username = host_request[0].username
        print salt_ip, jumper_ip

        salt_master_ip = ["120.76.130.53"]
        #### user ssh-keygen
        user_cmd = "ssh-keygen -t dsa -P '' -f /home/" + username + "/.ssh/id_rsa"
        #### cp 文件
        cp_cmd = "cp /home/" + username + "/.ssh/id_rsa.pub /home/" + username + "/.ssh/authorized_keys"

        cf = ConfigParser.ConfigParser()
        cf.read("/web/CMDB/app/backend/config.ini")
        salt_user = cf.get("saltstack", "user")
        salt_pass = cf.get("saltstack", "pass")

        #### 循环多个 跳板机
        for ip_num in range(0, len(salt_master_ip)):
            salt_url = "https://" + salt_master_ip[ip_num] + ":8888"
            sapi = SaltAPI(url=salt_url, username=salt_user, password=salt_pass)
            #### 创建用户
            print sapi.remote_execution(hostname, 'user.add', {'arg1': username})
            #### 生成 ssh-key
            print sapi.remote_execution(hostname, 'cmd.run',
                                        {'arg1': user_cmd,
                                         'arg2': 'runas=' + username})
            ### 生成 authrized_keys
            print sapi.remote_execution(hostname, 'cmd.run',
                                        {'arg1': cp_cmd,
                                         'arg2': 'runas=' + username})

            ### 修改 sudoers 添加 username sudo 权限

        host_request.update(status=request_status)

    content = "您所申请的主机："+ str(request_nick_name_list) +"已经通过审核,可以通过跳板机登陆"

    send_mail("admin", request_user, "主机申请", content)

    return HttpResponseRedirect("/app/get_approval_accept_page/")
