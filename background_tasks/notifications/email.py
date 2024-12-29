from asgiref.sync import async_to_sync
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

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

    def create_message(
        self,
        recepients: list[str],
        subject: str,
        body: str,
    ) -> MessageSchema:
        return MessageSchema(
            recipients=recepients,
            subject=subject,
            body=body,
            subtype=MessageType.plain,
        )

    def create_reset_token_message(
        self,
        user_email: str,
        reset_token: str,
    ) -> str:
        body = (
            f"This is your reset token:\n\n{reset_token}\n\n"
            "Please use it while accessing the following "
            "link to reset your password.\n\n"
            f"{settings.app.domain}/auth/reset-password"
        )
        return self.create_message(
            recepients=[user_email],
            subject="Async_service_v2: Password Reset.",
            body=body,
        )

    def create_verification_url_message(
        self,
        user_email: str,
        verification_url: str,
    ) -> str:
        body = (
            "To verify your email address please follow the link below: \n\n"
            f"{verification_url}"
        )
        return self.create_message(
            recepients=[user_email],
            subject="Async_service_v2: Email verificatoin.",
            body=body,
        )


email_service = EmailService()
