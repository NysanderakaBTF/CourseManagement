from celery import Celery
from celery.schedules import crontab

from core.config import config

celery_app = Celery('celery_app',
                    broker=config.CELERY_BROKER_URL,
                    backend=config.CELERY_BACKEND_URL
                    )

celery_app.conf.imports = ['celery_app.tasks']

celery_app.conf.task_routes = {"celery_app.celery_worker.test_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)
celery_app.conf.beat_schedule = {
    'run-every-30-minutes': {
        'task': 'send_new_courses',
        'schedule': crontab(minute='*/1'),
    },
    'run-every-10-minutes': {
        'task': 'send_updated_courses',
        'schedule': crontab(minute='*/1'),
    },
}
