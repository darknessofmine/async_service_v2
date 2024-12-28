
from asgiref.sync import async_to_sync

from .notifications import mail
from .celery import celery_app


@celery_app.task()
def send_reset_token(*args, **kwargs):
    message = mail.create_reset_token_message(*args, **kwargs)
    async_to_sync(mail.fast_mail.send_message)(message)


@celery_app.task()
def send_verification_url(*args, **kwargs):
    message = mail.create_verification_url_message(*args, **kwargs)
    async_to_sync(mail.fast_mail.send_message)(message)
