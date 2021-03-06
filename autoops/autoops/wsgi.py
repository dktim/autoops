#/usr/bin/python2.7
"""
WSGI config for UAT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoops.settings")
sys.path.insert(0,'/root/Python-2.7.12/uat/lib/python2.7/lib-dynload')
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
