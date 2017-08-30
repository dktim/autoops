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
from account.views import mylogin
from monitor.views import login
from django.conf.urls import url,include
from monitor.views import host_restart
from django.contrib import admin
urlpatterns = [
 url(r"^$",login,name="auto_login"),
 url(r'host_restart',host_restart),
 url(r"^login",login,name='index_login'),
 url(r"^account/",include('account.urls')), 
 url(r"^hiasset/",include('hiasset.urls')), 
 url(r"^execute/",include('execute.urls')),
  url(r"^monitor/",include('monitor.urls')),
   url(r"^controller/",include('controller.urls')),
 url(r"^jobs/",include('jobs.urls')),
 url(r"^deploy/",include('deploy.urls')), 
 url(r"^filemanage/",include('filemanage.urls')),
 url(r'^admin/', admin.site.urls),
url(r'^backend/',include('backend.urls')),
   
   
             
          
]

