

from __future__ import absolute_import
import sys
import os
import django
from autoops import settings
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoops.settings')
django.setup()

app =Celery('autoops')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))