import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'notify_week_posts_every_monday_8am': {
        'task': 'news.tasks.notify_week_posts',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
    'clear_task_redis_every_10_minutes': {
        'task': 'news.tasks.clear_task_redis',
        'schedule': crontab(minute='*/10'),
    }
}

app.autodiscover_tasks()
