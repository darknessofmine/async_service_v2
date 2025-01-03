from asgiref.sync import async_to_sync
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from core.settings import settings


class EmailService(FastMail):
    def __init__(self) -> None:
        self.config = ConnectionConfig(**settings.email.model_dump())

    @async_to_sync
    async def send_message(
        self,
        message: MessageSchema,
        template_name: str | None = None,
    ) -> None:
        await super().send_message(message, template_name)

    @staticmethod
    def create_message(
        recipients: list[EmailStr],
        subject: str,
        body: str,
    ) -> MessageSchema:
        return MessageSchema(
            recipients=recipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain,
        )

    def create_reset_token_message(
        self,
        user_email: EmailStr,
        reset_token: str,
    ) -> MessageSchema:
        body = (
            f"This is your reset token:\n\n{reset_token}\n\n"
            "Please use it while accessing the following "
            "link to reset your password.\n\n"
            f"{settings.app.domain}/auth/reset-password"
        )
        return self.create_message(
            recipients=[user_email],
            subject="Async_service_v2: Password Reset.",
            body=body,
        )

    def create_verification_url_message(
        self,
        user_email: EmailStr,
        verification_url: str,
    ) -> MessageSchema:
        body = (
            "To verify your email address please follow the link below: \n\n"
            f"{verification_url}"
        )
        return self.create_message(
            recipients=[user_email],
            subject="Async_service_v2: Email verificatoin.",
            body=body,
        )


email_service = EmailService()
