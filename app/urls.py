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
    url(r'^add_host/$', views.add_host),
    url(r'^sync_host/$', views.sync_host),

    url(r'^user_list/$', views.user_list),
    url(r'^modify_user_permissions/$', views.modify_user_permissions),

    url(r'^get_approval_request/$', views.get_approval_request),
    url(r'^get_approval_accept_page/$', views.get_approval_accept_page),
    url(r'^change_idc/$', views.change_idc),
    url(r'^change_group/$', views.change_group),
    url(r'^approval_request/.*$', views.approval_request),
    url(r'^get_host_request_by_username/$', views.get_host_request_by_username),
    url(r'^approval_accept/$', views.approval_accept),
]
