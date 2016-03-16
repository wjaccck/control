__author__ = 'jinhongjun'

from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^exec', views.CmdViewSet),
    url(r'^exec/salt', views.Cmd_saltViewSet),
    url(r'^salt/key/all', views.Salt_key_all_ViewSet),
    url(r'^salt/key/accept', views.Salt_key_accept_ViewSet),
    url(r'^salt/key/delete', views.Salt_key_delete_ViewSet),
    url(r'^salt/minion/init', views.Salt_minion_init_ViewSet),
    url(r'^salt/module/name', views.Salt_module_name_ViewSet),
]
