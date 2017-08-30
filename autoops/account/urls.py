from django.conf.urls import patterns,url
from account.views import *
#from django.contrib.auth.views.login import *


urlpatterns=[
url(r'mylogin',mylogin,name='mylogin'),
url(r'logout',mylogout,name='logout'),
    url(r'add_user', add_user, name='add_user'),
    url(r'del_user', del_user, name='del_user'),
    url(r'set_password', set_password, name='set_password'),
    url(r'setup_user', setup_user, name='setup_user'),
    url(r'manage_user', add_user, name='manage_user'),

    url(r'^manage_business', manage_business,name='manage_business'),
    url(r'^modify_business', modify_business,name='modify_business'),
    url(r'^add_business', add_business,name='add_business'),
    url(r'^del_business', del_business,name='del_business'),

    url(r'^manage_privilege', manage_privilege,name='manage_privilege'),
    url(r'^modify_privilege', modify_privilege,name='modify_privilege'),
    url(r'^add_privilege', add_privilege,name='add_privilege'),
    url(r'^del_privilege', del_privilege,name='del_privilege'),
]
