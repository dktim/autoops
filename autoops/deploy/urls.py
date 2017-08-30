
from django.conf.urls import url,include
from deploy.views import regular_deploy,cron_deploy
urlpatterns=[
url(r'^regular_deploy',regular_deploy),
url(r'^cron_deploy',cron_deploy),
]
