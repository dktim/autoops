
from django.conf.urls import patterns,url
from execute.views import shell_cmd,shell_result,salt_runcmd,salt_result,jobs_his,test_celery
from .views import manage_file,upload_file,del_file,get_host_by_reg
#,del_file,upload_file
#from django.contrib.auth.views.login import *


urlpatterns=[

url(r'shell_cmd/$',shell_cmd),
    url(r'^manage_file*', manage_file,name='manage_file'),
    url(r'^del_file', del_file,name='del_file'),
    url(r'^upload_file', upload_file,name='upload_file'),    
    url(r'^get_host_by_reg', get_host_by_reg,name='get_host_by_reg'), 
]
