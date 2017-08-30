
from django.conf.urls import url,include
from jobs.views import regular_job,cron_job,cron_job_result
urlpatterns=[


url(r'regular_job',regular_job),
url(r'^cron_job$',cron_job),
url(r'cron_job_result',cron_job_result)
]
