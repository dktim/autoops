
from django.conf.urls import url,include
from group.views import *
urlpatterns=[

url(r'manage_group',manage_group),
url(r'del_group',del_group),
url(r'modify_group',modify_group),
url(r'add_group',add_group),
#url(r'manage_group',manage_group),





]
