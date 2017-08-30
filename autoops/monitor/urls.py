'''
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
'''
from django.conf.urls import url,include
from django.contrib import admin
from monitor.views import *

urlpatterns = [
url(r'yutouchan_index$',yutouchan_index,name='yutouchan'),
url(r'production_index',production_index,name='production'),
url(r'get_reg_action_history',get_reg_action_history),
url(r'get_hub_ajax_state',get_hub_ajax_state),
url(r'start_page_with_hub_state',start_page_with_hub_state,name='start_page_with_hub_state'),
url(r'index/(?P<id>\d+)/$',index,name='index'),
url(r'wls_monitor',wls_monitor),
url(r'security_port_monitor',query_all_server_port_status),
url(r'logstash_monitor',logstash_monitor),
url(r'server_list/',server_list,name='server_list'),
url(r'single_machine_jdbc_state',single_machine_jdbc_state),
url(r'single_machine_jms_state',single_machine_jms_state),
url(r'single_machine_lsn_state',single_machine_lsn_state),
url(r'single_machine_hub_state',single_machine_hub_state),
url(r'start_page_with_lsn_state',start_page_with_lsn_state),
url(r'jms_state/',get_jms_state,name='jms_state'),
url(r'listener_state/',get_listener_state,name='listener_state'),
url(r'hub_state/',get_hub_state,name='hub_state'),
url('jdbc_status2',jdbc_status2,name='jdbc_status2'),
url(r'get_reg_info/',get_reg_info,name='get_reg_info'),
url(r'jdbc_status3/',jdbc_status3,name='jdbc_status3'),
url(r'get_jdbc_state',get_jdbc_state),
url(r'single_machine',single_machine),
url(r'get_jms_state',get_jms_state),
url(r'get_jms_ajax_state',get_jms_state_ajax),
url(r'lsn_status',lsn_status,name='lsn_status'),
url(r'get_lsn_ajax_state',get_lsn_ajax_state,name='get_lsn_ajax_state'),
url(r'get_jdbc1_state_at_start',get_jdbc_state_at_start,name='get_jdbc_state_at_start'),
url(r'start_page_with_jms_state',start_page_with_jms_state,name='start_page_with_jms_state'),
url(r'hourly_jms_state',get_jms_state_by_hour),
url(r'hourly_jdbc_state',get_jdbc_state_by_hour),
url(r'hourly_hub_state',get_hub_state_by_hour),
url(r'hourly_lsn_state',get_lsn_state_by_hour), 
url(r'production_index',production_index),
url(r'thread_monitor',thread_monitor),
    
]
