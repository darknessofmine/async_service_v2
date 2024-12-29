
from .notifications.email import email_service
from .celery import celery_app


@celery_app.task()
def send_reset_token(email: str, token: str) -> None:
    message = email_service.create_reset_token_message(email, token)
    email_service.send_message(message)


@celery_app.task()
def send_verification_url(email: str, url: str) -> None:
    message = email_service.create_verification_url_message(email, url)
    email_service.send_message(message)
