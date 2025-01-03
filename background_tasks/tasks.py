from fastapi import UploadFile
from pydantic import EmailStr

from .files.file_service import file_service
from .notifications.email_service import email_service
from .celery import celery_app


@celery_app.task
def send_reset_token(email: EmailStr, token: str) -> None:
    message = email_service.create_reset_token_message(email, token)
    email_service.send_message(message)


@celery_app.task
def send_verification_url(email: EmailStr, url: str) -> None:
    message = email_service.create_verification_url_message(email, url)
    email_service.send_message(message)


@celery_app.task
def save_profile_image(image_to_save: UploadFile, image_url: str) -> None:
    file_service.save_file(image_to_save, image_url)
