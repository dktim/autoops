
from django.conf.urls import url,include
from backend.views import query_machine, multitask_cmd,multitask_res
from backend.views import update_machine_info

from backend.views import add_machine_info,multi_host,query_file_h
from backend.views import test
urlpatterns=[

url(r'query_machine',query_machine),

url(r'add_machineinfo',add_machine_info),
url(r'^update_machine_info',update_machine_info),
url(r'multi_host',multi_host),
url(r'multitask_cmd',multitask_cmd,name='multi_task_cmd'),
url(r'multitask_res',multitask_res,name='multi_task_res'),

url(r'query_file_h',query_file_h,name='query_file'),
url('test',test),

]
