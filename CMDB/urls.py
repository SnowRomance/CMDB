"""CMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import sys, os
sys.path.append(os.getcwd())
from app import urls as app_urls
from account import urls as account_urls
from order import urls as order_urls
from approval import urls as approval_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include(app_urls)),
    url(r'^account/', include(account_urls)),
    url(r'^order/', include(order_urls)),
    url(r'^approval/', include(approval_urls)),
]
