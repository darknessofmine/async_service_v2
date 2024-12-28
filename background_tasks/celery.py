from celery import Celery

from core.settings import settings


celery_app = Celery()

celery_app.conf.update(
    broker_url=settings.redis.url,
    result_backend=settings.redis.url,
    broker_connection_retry_on_startup=True,
)
