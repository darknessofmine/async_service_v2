from celery import Celery

from core.settings import settings


celery_app = Celery()

celery_app.conf.broker_url = settings.redis.url
celery_app.conf.result_backend = settings.redis.url
