from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab  
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')

app = Celery('restaurant')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'America/Santiago'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_daily_menu': {
        'task': 'api.tasks.send_daily_menu',
        'schedule': crontab(hour=11, minute=30),
    #    'schedule': timedelta(seconds=15),
    
    },
}