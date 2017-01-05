# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from app.models import *
import MySQLdb as mysql
from CMDB.settings_config import dbconfig, saltconfig
from app.backend.saltapi import SaltAPI
from django.contrib.auth.models import User
from order.models import *
from account.models import *
from approval.models import *
from common.views import get_user_dict, get_host_dict
from datetime import timedelta
import ConfigParser
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Create your views here.

config_list = dbconfig()
db = mysql.connect(host=config_list["host"], user=config_list["user"], passwd=config_list["pass"],
                   db=config_list["name"], charset="utf8")
db.autocommit(True)
c = db.cursor()

config_list_sal = saltconfig()
sapi = SaltAPI(url=config_list_sal["salt_url"], username=config_list_sal["salt_user"],
               password=config_list_sal["salt_pass"])


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
        group_name = group_list[0].group_name
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


#### 获取 申请主机页面
def get_approval_request(request):
    idc_list = Idc.objects.all()
    group_list = []
    host_list = []
    if idc_list:
        idc_name = idc_list[0].idc_name
        group_list = Group.objects.filter(idc_name=idc_name)
        if group_list:
            group_name = group_list[0].group_name
            c.execute(
                "select ah.* from app_hostlist ah where ah.hostname not in (select ahq.hostname from approval_hostrequest ahq where ahq.username = '" + str(
                    request.user) + "' and ahq.create_time > DATE_ADD(CURDATE(), Interval -1 month) and ahq.status !=2) and ah.group_name='" + str(
                    group_name) + "' and ah.idc_name='" + str(idc_name) + "'")

            for filterhost in c.fetchall():
                host = get_host_dict(filterhost)
                host_list.append(host)
    return render_to_response("approval/approval_request.html",
                              {"user": request.user, "idc_list": idc_list, "group_list": group_list,
                               "host_list": host_list})


#### 获取申请主机列表
def approval_request_list(request):
    user = request.user
    host_requests_list = []
    host_requests = HostRequest.objects.filter(username=user)
    if host_requests:
        for host_request_object in host_requests:
            host_request = {}
            host_request["nick_name"] = host_request_object.nick_name
            host_request["status"] = host_request_object.status
            host_request["create_time"] = host_request_object.create_time
            host_list = HostList.objects.filter(hostname=host_request_object.hostname)
            if host_list:
                host_request["idc_name"] = host_list[0].idc_name
                host_request["group_name"] = host_list[0].group_name
                host_request["ip"] = host_list[0].ip
                host_request["inner_ip"] = host_list[0].inner_ip
            host_requests_list.append(host_request)

    print host_requests_list
    return render_to_response("approval/approval_request_list.html",
                              {"user": user, "host_requests_list": host_requests_list})


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
        if not HostRequest.objects.filter(hostname=hostname, username=username):
            host_request = HostRequest()
            host_request.hostname = hostname
            host_request.username = username
            host_request.nick_name = nickname
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
    host_requests = []
    c.execute("select distinct(ahq.username) from approval_hostrequest ahq")
    for request_user in c.fetchall():
        request_user_list.append(request_user[0])

    if request_user_list:
        host_requests = HostRequest.objects.filter(status=0, username=request_user_list[0])
    return render_to_response("approval/approval_deal.html", locals())


def get_approval_accept_page_by_username(request):
    host_requests = []
    username = request.POST.get("username")
    if User.objects.filter(username=username):
        host_requests = HostRequest.objects.filter(status=0, username=username)
    host_requests_dict = {}
    inum = 0
    for host_request in host_requests:
        host_requests_dict[str(inum)] = host_request.__unicode__()
        inum += 1
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(json.dumps(host_requests_dict))
    return response


def approval_accept(request):
    requestid_list = request.GET.get("requestid_list")
    request_status = request.GET.get("request_status")
    request_user = request.GET.get("request_user")
    request_nick_name_list = []
    requestid_list = requestid_list.split(",")
    for key in range(0, len(requestid_list) - 1):
        host_request = HostRequest.objects.filter(id=requestid_list[key])
        request_nick_name_list.append(host_request[0].nick_name)
        if request_status == "1":
            hostname = host_request[0].hostname
            create_time = host_request[0].create_time

            c.execute("select auth_user.* from auth_user where username='" + str(request_user) + "'")
            filteruser = c.fetchone()
            if filteruser is not None:
                user = get_user_dict(filteruser)
                email = user["email"]
                ### 获取 user
                user = ""
                user_part = email.split('@')[0]
                for user_p in user_part.split('.'):
                    user = user + user_p

            #### user ssh-keygen
            user_cmd = "ssh-keygen -t dsa -P '' -f /home/" + user + "/.ssh/id_rsa"
            #### chmod u+w /etc/sudoers
            chw_cmd = "chmod u+w /etc/sudoers"
            #### 添加 sudo 权限
            sed_cmd = "sed -i '$a " + user + "    ALL=(ALL)       NOPASSWD:ALL ' /etc/sudoers"
            #### chmod u-w /etc/sudoers
            chw_cut_cmd = "chmod u-w /etc/sudoers"

            cf = ConfigParser.ConfigParser()
            cf.read("/web/CMDB/app/backend/config.ini")

            salt_url = cf.get("saltstack", "url")
            salt_user = cf.get("saltstack", "user")
            salt_pass = cf.get("saltstack", "pass")

            sapi = SaltAPI(url=salt_url, username=salt_user, password=salt_pass)
            #### 创建用户
            print sapi.remote_execution(hostname, 'user.add', {'arg1': user})
            aDay = timedelta(days=30)
            time_now = create_time + aDay
            print sapi.remote_execution(hostname, 'cmd.run', {'arg1': "usermod -e " + str(time_now) + " " + user})
            #### 生成 ssh-key
            print sapi.remote_execution(hostname, 'cmd.run',
                                        {'arg1': user_cmd,
                                         'arg2': 'runas=' + user})
            #### cp.get_file authrized_keys
            print sapi.remote_execution(hostname, 'cp.get_file',
                                        {'arg1': "salt://" + user + "_cmdb_login_id_rsa_pub",
                                         'arg2': "/home/" + user + "/.ssh/authorized_keys"})

            #### cp.get_file id_rsa
            print sapi.remote_execution(hostname, 'cp.get_file',
                                        {'arg1': "salt://" + user + "_cmdb_login_id_rsa",
                                         'arg2': "/home/" + user + "/.ssh/id_rsa"})

            #### cp.get_file id_rsa.pub
            print sapi.remote_execution(hostname, 'cp.get_file',
                                        {'arg1': "salt://" + user + "_cmdb_login_id_rsa_pub",
                                         'arg2': "/home/" + user + "/.ssh/id_rsa.pub"})

            #### chowd user:user .ssh
            print sapi.remote_execution(hostname, 'cmd.run',
                                        {'arg1': "chown -R " + user + ":" + user + " /home/" + user + "/.ssh"})

            ### 修改 sudoers 添加 username sudo 权限
            print sapi.remote_execution(hostname, 'cmd.run',
                                        {'arg1': chw_cmd,
                                         'arg2': 'runas=root'})

            print sapi.remote_execution(hostname, 'cmd.run',
                                        {'arg1': sed_cmd,
                                         'arg2': 'runas=root'})

            print sapi.remote_execution(hostname, 'cmd.run',
                                        {'arg1': chw_cut_cmd,
                                         'arg2': 'runas=root'})
            # lease = Lease()
            # lease.hostname = hostname
            # lease.username = request_user
            # lease.save()
        host_request.update(status=request_status)

    #### send mail
    content = "您所申请的主机：" + str(request_nick_name_list) + "已经通过审核,可以通过跳板机登陆"
    send_mail("admin", request_user, "主机申请", content)

    return HttpResponseRedirect("/approval/get_approval_accept_page/")
