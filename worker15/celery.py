from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker15.settings')
app = Celery('worker15')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'Check_WS_24H': {
        'task': 'tasker.views.check_dates',
        'schedule': crontab(hour=1, minute=0)
    },
}
#app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))