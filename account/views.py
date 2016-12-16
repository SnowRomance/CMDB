# -*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
import time
from forms import RegisterForm
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.backend.saltapi import *
import ConfigParser
import send_email


# Create your views here.

def index(request):
    pass

def ssh_key(email):
    salt_master_ip = ["120.76.130.53"]
    jumper_ip = ["iZ940kub0iuZ"]
    ### 获取 user
    user = ""
    user_part = email.split('@')[0]
    for user_p in user_part.split('.'):
        user = user + user_p
    #### user ssh-keygen
    user_cmd = "ssh-keygen -t dsa -P '' -f /home/" + user + "/.ssh/id_rsa"
    #### cp 文件
    cp_cmd = "cp /home/"+ user+"/.ssh/id_rsa.pub /home/"+user+"/.ssh/authorized_keys"
    #### mv 文件
    mv_cmd = "mv /var/cache/salt/master/minions/"+user+"/files/home/"+user+"/.ssh/id_rsa /web/CMDB/static/upload/"+user+"_cmdb_login_id_rsa"

    cf = ConfigParser.ConfigParser()
    cf.read("/web/CMDB/app/backend/config.ini")
    salt_user = cf.get("saltstack", "user")
    salt_pass = cf.get("saltstack", "pass")

    #### 循环多个 跳板机
    for ip_num in range(0, len(salt_master_ip)):
        salt_url = "https://" + salt_master_ip[ip_num] + ":8888"
        sapi = SaltAPI(url=salt_url, username=salt_user, password=salt_pass)
        #### 创建用户
        print sapi.remote_execution(jumper_ip[ip_num], 'user.add', {'arg1': user})
        #### 生成 ssh-key
        print sapi.remote_execution(jumper_ip[ip_num], 'cmd.run',
                                    {'arg1': user_cmd,
                                     'arg2': 'runas='+user})
        ### 生成 authrized_keys
        print sapi.remote_execution(jumper_ip[ip_num], 'cmd.run',
                                    {'arg1': cp_cmd,
                                    'arg2': 'runas='+user})

    salt_url = "https://" + salt_master_ip[0] + ":8888"
    sapi = SaltAPI(url=salt_url, username=salt_user, password=salt_pass)
    print sapi.remote_execution(jumper_ip[0], 'cp.push', '/home/'+ user +'/.ssh/id_rsa')
    # print sapi.remote_execution(salt_master_ip[0], 'cmd.run',
    #                             {'arg1': "sz /var/cache/salt/master/minions/"+jumper_ip[0]+"/files/home/"+user+"/.ssh/id_rsa",
    #                             })
    print sapi.remote_execution(jumper_ip[0], 'cmd.run', {'arg1': mv_cmd})

    mail_host = 'smtp.exmail.qq.com'
    mail_user = 'yangjun.liu@quvideo.com'
    mail_pass = 'Lyj!2015'

    se = send_email.EmailSender(mail_host, mail_user, mail_pass)
    se.send("cmdb 使用", email, jumper_ip)
    se.close()

# @login_required()
def userRegister(request):
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print curtime

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
            # errors.extend(registerForm.errors.values())
            #     return render_to_response("account/userregister.html",
            #                               {'registerForm':registerForm, 'curtime': curtime, 'username': username, 'email': email, 'errors': errors})
            # if password1 != password2:
            #     errors.append("两次输入的密码不一致!")
            #     return render_to_response("account/userregister.html",
            #                               {'registerForm':registerForm, 'curtime': curtime, 'username': username, 'email': email, 'errors': errors})
            #
            # filterResult = User.objects.filter(username=username)
            # if len(filterResult) > 0:
            #     errors.append("用户名已存在")
            #     return render_to_response("account/userregister.html",
            #                               {'registerForm':registerForm, 'curtime': curtime, 'username': username, 'email': email, 'errors': errors})

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
            ssh_key(email)
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
