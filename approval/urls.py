from django.conf.urls import url
import views

urlpatterns = [
    url(r'^get_approval_request/$', views.get_approval_request),
    url(r'^approval_request_list/$', views.approval_request_list),
    url(r'^get_approval_accept_page/$', views.get_approval_accept_page),
    url(r'^get_approval_accept_page_by_username/$', views.get_approval_accept_page_by_username),
    url(r'^change_idc/$', views.change_idc),
    url(r'^change_group/$', views.change_group),
    url(r'^approval_request/.*$', views.approval_request),
    url(r'^approval_accept/$', views.approval_accept),
]
