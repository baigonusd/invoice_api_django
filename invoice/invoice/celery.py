from __future__ import absolute_import, unicode_literals

import os
from dotenv import load_dotenv, find_dotenv
from celery import Celery

load_dotenv(dotenv_path=find_dotenv())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoice.settings')

celery = Celery('invoice', broker=os.environ.get('BROKER_URL'),
                backend=os.environ.get('BACKEND_URL'))

celery.config_from_object('django.conf:settings', namespace='CELERY')

celery.autodiscover_tasks()
