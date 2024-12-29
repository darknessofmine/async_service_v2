
from .notifications.email import email_service
from .celery import celery_app


@celery_app.task()
def send_reset_token(*args, **kwargs):
    message = email_service.create_reset_token_message(*args, **kwargs)
    email_service.send_message(message)


@celery_app.task()
def send_verification_url(*args, **kwargs):
    message = email_service.create_verification_url_message(*args, **kwargs)
    email_service.send_message(message)
