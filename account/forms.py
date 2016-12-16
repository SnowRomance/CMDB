# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, label='用户名：', max_length=30, help_text="请输入用户名", error_messages={'required':u'别名不能为空'})
    password1 = forms.CharField(required=True, label='密码：',widget=forms.PasswordInput(), help_text="请输入密码", error_messages={'required':u'密码不能为空'})
    password2 = forms.CharField(required=True, label='确认密码：',widget=forms.PasswordInput(), help_text="请输入确认密码", error_messages={'required':u'确认密码不能为空'})
    email = forms.EmailField(required=True, label='邮箱', help_text="请输入邮箱", error_messages={'required':u'邮箱不能为空'})
    phone = forms.CharField(required=True, label='手机号码', help_text="请输入手机号码", error_messages={'required':u'手机号码不能为空'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        filterResult = User.objects.filter(username=username)
        if len(filterResult) > 0:
            raise forms.ValidationError("用户名已存在！")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致!")
        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise forms.ValidationError("手机号码需要 11 位！")
        return phone