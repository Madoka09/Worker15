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
        'task': 'tasker.views.app_status',
        'schedule': crontab(hour=1, minute=0),
        #'args': request
    },
}
#app.conf.timezone = 'UTC'

'''
@app.on_after_configure.connect 
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )
'''

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))