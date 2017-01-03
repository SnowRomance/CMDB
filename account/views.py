# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import time
from forms import RegisterForm, LoginForm
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib import auth
from app.backend.saltapi import *
import ConfigParser
import send_email


# Create your views here.

def index(request):
    pass


# def ssh_key(email):
#     salt_master_ip = ["120.76.130.53"]
#     salt_master_name = ["iZ94fa46qhcZ"]
#
#     idc_list = Idc.objects.all()
#     jumper_name = []
#     for idc in idc_list:
#         host_list = HostList.objects.filter(ip=idc.jumper_ip)
#         jumper_name.append(host_list[0].hostname)
#
#     ### 获取 user
#     user = ""
#     user_part = email.split('@')[0]
#     for user_p in user_part.split('.'):
#         user = user + user_p
#     #### user ssh-keygen
#     user_cmd = "ssh-keygen -t dsa -P '' -f /home/" + user + "/.ssh/id_rsa"
#     #### cp 文件
#     cp_cmd = "cp /home/" + user + "/.ssh/id_rsa.pub /home/" + user + "/.ssh/authorized_keys"
#     #### mv 文件
#     mv_cmd = "mv /var/cache/salt/master/minions/" + jumper_name[0] + "/files/home/" + user + \
#              "/.ssh/id_rsa /web/CMDB/static/upload/" + user + "_cmdb_login_id_rsa"
#
#     mv_cmd_pub = "mv /var/cache/salt/master/minions/" + jumper_name[0] + "/files/home/" + user + \
#              "/.ssh/id_rsa_pub /web/CMDB/static/upload/" + user + "_cmdb_login_id_rsa_pub"
#
#     cf = ConfigParser.ConfigParser()
#     cf.read("/web/CMDB/app/backend/config.ini")
#     salt_user = cf.get("saltstack", "user")
#     salt_pass = cf.get("saltstack", "pass")
#
#     #### 循环多个 跳板机
#     for ip_num in range(0, len(salt_master_ip)):
#         salt_url = "https://" + salt_master_ip[ip_num] + ":8888"
#         sapi = SaltAPI(url=salt_url, username=salt_user, password=salt_pass)
#         #### 创建用户
#         print sapi.remote_execution(jumper_name[ip_num], 'user.add', {'arg1': user})
#         #### 生成 ssh-key
#         print sapi.remote_execution(jumper_name[ip_num], 'cmd.run',
#                                     {'arg1': user_cmd,
#                                      'arg2': 'runas=' + user})
#         ### 生成 authrized_keys
#         print sapi.remote_execution(jumper_name[ip_num], 'cmd.run',
#                                     {'arg1': cp_cmd,
#                                      'arg2': 'runas=' + user})
#         #### rsa
#         print sapi.remote_execution(jumper_name[ip_num], 'cp.push', {'arg1': '/home/' + user + '/.ssh/id_rsa'})
#         print sapi.remote_execution(salt_master_name[ip_num], 'cmd.run', {'arg1': mv_cmd})
#
#         #### rsa.pub
#         print sapi.remote_execution(jumper_name[ip_num], 'cp.push', {'arg1': '/home/' + user + '/.ssh/id_rsa.pub'})
#         print sapi.remote_execution(salt_master_name[ip_num], 'cmd.run', {'arg1': mv_cmd_pub})
#
#     mail_host = cf.get('admin_email', "mail_host")
#     mail_user = cf.get('admin_email', "mail_user")
#     mail_pass = cf.get('admin_email', "mail_pass")
#
#     se = send_email.EmailSender(mail_host, mail_user, mail_pass)
#     se.send("cmdb 使用", [email], ["iZ940kub0iuZ"])
#     se.close()


def get_ssh_key(email):
    cf = ConfigParser.ConfigParser()
    cf.read("/web/CMDB/app/backend/config.ini")

    salt_master_ip = cf.get("saltstack", "salt_master_ip")
    salt_master_name = cf.get("saltstack", "salt_master_name")

    ### 获取 user
    user = ""
    user_part = email.split('@')[0]
    for user_p in user_part.split('.'):
        user = user + user_p
    #### user ssh-keygen
    user_cmd = "ssh-keygen -t dsa -P '' -f /home/" + user + "/.ssh/id_rsa"
    #### cp 文件
    cp_cmd = "cp /home/" + user + "/.ssh/id_rsa.pub /home/" + user + "/.ssh/authorized_keys"
    #### mv 文件
    mv_cmd = "mv /home/" + user + "/.ssh/id_rsa /web/CMDB/static/upload/" + user + "_cmdb_login_id_rsa"

    mv_cmd_pub = "mv /home/" + user + "/.ssh/id_rsa.pub /web/CMDB/static/upload/" + user + "_cmdb_login_id_rsa_pub"

    salt_user = cf.get("saltstack", "user")
    salt_pass = cf.get("saltstack", "pass")


    salt_url = "https://" + salt_master_ip + ":8888"
    sapi = SaltAPI(url=salt_url, username=salt_user, password=salt_pass)
    #### 创建用户
    print sapi.remote_execution(salt_master_name, 'user.add', {'arg1': user})
    #### 生成 ssh-key
    print sapi.remote_execution(salt_master_name, 'cmd.run',
                                {'arg1': user_cmd,
                                 'arg2': 'runas=' + user})
    ### 生成 authrized_keys
    print sapi.remote_execution(salt_master_name, 'cmd.run',
                                {'arg1': cp_cmd,
                                 'arg2': 'runas=' + user})
    #### rsa
    print sapi.remote_execution(salt_master_name, 'cmd.run', {'arg1': mv_cmd})

    #### rsa.pub
    print sapi.remote_execution(salt_master_name, 'cmd.run', {'arg1': mv_cmd_pub})

    mail_host = cf.get('admin_email', "mail_host")
    mail_user = cf.get('admin_email', "mail_user")
    mail_pass = cf.get('admin_email', "mail_pass")

    se = send_email.EmailSender(mail_host, mail_user, mail_pass)
    se.send("cmdb 使用", [email])
    se.close()


# @login_required()
def userRegister(request):
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    errors = []
    username = ""
    email = ""
    if request.method == 'POST':
        print "if Register"
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')

        registerForm = RegisterForm(
            {'username': username, 'password1': password1, 'password2': password2, 'email': email, 'phone': phone})
        try:
            if not registerForm.is_valid():
                return render_to_response("account/userregister.html",
                                          {'registerForm': registerForm, 'curtime': curtime, 'username': username,
                                           'email': email, 'errors': errors})

            user = User()
            user.username = username
            user.set_password(password1)
            user.email = email
            user.save()
            # 用户扩展信息 profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.phone = phone
            profile.save()
            get_ssh_key(email)
            # 登录前需要先验证
            newUser = auth.authenticate(username=username, password=password1)
            if newUser is not None:
                auth.login(request, newUser)
                return HttpResponseRedirect("/app/index/")
        except Exception, e:
            errors.append(str(e))
            return render_to_response("account/userregister.html",
                                      {'registerForm': registerForm, 'curtime': curtime, 'username': username,
                                       'email': email, 'errors': errors})

    else:
        print "else Register"
        registerForm = RegisterForm()
        return render_to_response("account/userregister.html",
                                  {'registerForm': registerForm, 'curtime': curtime, 'username': username,
                                   'email': email, 'errors': errors})


def login(request):
    errors = []
    username = ""
    password = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        loginForm = LoginForm({'username': username, 'password': password})
        try:
            if not loginForm.is_valid():
                return render_to_response("account/login.html",
                                          {'loginForm': loginForm, 'username': username, 'password': password,
                                           'errors': errors})

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect("/app/index/")
        except Exception, e:
            errors.append(str(e))
            return render_to_response("account/login.html",
                                      {'loginForm': loginForm, 'username': username, 'password': password,
                                       'errors': errors})
    else:
        loginForm = LoginForm()
        return render_to_response("account/login.html",
                                  {'loginForm': loginForm, 'username': username, 'password': password,
                                   'errors': errors})
