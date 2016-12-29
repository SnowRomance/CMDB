from django.conf.urls import url
import views

urlpatterns = [
    url(r'^inbox/$', views.inbox),
    url(r'^outbox/$', views.outbox),
    url(r'^change_status/$', views.change_status),
    url(r'^get_send_page/$', views.get_send_page),
    url(r'^send/$', views.send),
]