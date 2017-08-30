"""UAT URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from monitor.views import *
from controller.views import *
urlpatterns = [
    url(r'reg_restart',restart_reg,name='start_reg'),
    url(r'reg_restart_detail',reg_restart_detail),
    url('app_cont',app_cont,name='app_cont'),
    url(r'get_node_state',get_node_state,name='get_node_state'),
    url(r'start_node',node_start,name='node_start'),
    url(r'stop_node',node_stop,name='node_stop'),
    url(r'get_server_detail',get_server_detail),
    url(r"machineinfo/(?P<reg>\w+)/$",machineinfo_list),
    url(r"get_server_open_status",get_server_open_status,name='get_server_open_status'),
    url(r'restart_result',restart_result),
    url(r'appstatus/(?P<regname>\S+)/(?P<ipaddress>\S+)/(?P<page>[0-9]+)/$',appStatus),
    url(r'modify_app_status',modify_app_status),
    
]
