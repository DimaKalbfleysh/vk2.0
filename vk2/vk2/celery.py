import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vk2.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('vk2', broker='redis://127.0.0.1:6379/0')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.

