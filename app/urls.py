from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index),

    url(r'^idc/$', views.idc),
    url(r'^get_add_idc_page/$', views.get_add_idc_page),
    url(r'^add_idc/$', views.add_idc),
    url(r'^modify_idc_remark/$', views.modify_idc_remark),

    url(r'^group/$', views.group),
    url(r'^get_add_group_page/$', views.get_add_group_page),
    url(r'^add_group/$', views.add_group),
    url(r'^modify_group_remark/$', views.modify_group_remark),

    url(r'^host_list/$', views.host_list),
    url(r'^get_add_host_page/$', views.get_add_host_page),
    url(r'^sync_host/$', views.sync_host),
]
