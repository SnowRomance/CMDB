from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^register/$', views.userRegister),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),

    url(r'^user_list/$', views.user_list),
    url(r'^modify_user_permissions/$', views.modify_user_permissions),
]
