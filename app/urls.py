from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^idc/$', views.idc),
    url(r'^get_add_idc_page/$', views.get_add_idc_page),
    url(r'^add_idc/$', views.add_idc)
]
