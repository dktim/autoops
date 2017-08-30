
from django.conf.urls import patterns,url
from execute.views import shell_cmd,shell_result,salt_runcmd,salt_result,jobs_his,test_celery
from views import test_celery
#from django.contrib.auth.views.login import *


urlpatterns=[

url(r'shell_cmd/$',shell_cmd),
    url(r'^minions_salt_runcmd', salt_runcmd, name='salt_runcmd'),
    url(r'^minions_shell_result', shell_result, name='shell_result'),
   url(r'^minions_salt_result', salt_result, name='salt_result'),
   url(r'^jobs_his',jobs_his),
    url(r'^test_celery',test_celery)
   # url(r'^get_history/([0|1])', views.get_history, name='get_history'),
]
