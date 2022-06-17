import os
from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1') #https://stackoverflow.com/questions/45744992/celery-raises-valueerror-not-enough-values-to-unpack

app = Celery('simpleapp')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'weekly_mail': {
        'task':'simpleapp.tasks.weekly_mail',
        'schedule':crontab(hour = 10, minute = 0, day_of_week='monday'), #в задании было 8 утра в понедельник, но это слишком рано и жестоко, я не могу пойти на такое.
        'args':(),
    }
}
app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks()