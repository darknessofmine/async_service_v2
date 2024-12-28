from asgiref.sync import async_to_sync
from celery import Celery

from .notifications import mail
from core.settings import settings


celery_app = Celery()

celery_app.conf.update(
    broker_url=settings.redis.url,
    result_backend=settings.redis.url,
    broker_connection_retry_on_startup=True,
)


@celery_app.task()
def send_reset_token(*args, **kwargs):
    message = mail.create_reset_token_message(*args, **kwargs)
    async_to_sync(mail.fast_mail.send_message)(message)


@celery_app.task()
def send_verification_url(*args, **kwargs):
    message = mail.create_verification_url_message(*args, **kwargs)
    async_to_sync(mail.fast_mail.send_message)(message)
