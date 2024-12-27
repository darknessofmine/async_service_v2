from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from core.settings import settings


fast_mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail.MAIL_USERNAME,
    MAIL_PASSWORD=settings.mail.MAIL_PASSWORD,
    MAIL_FROM=settings.mail.MAIL_FROM,
    MAIL_PORT=settings.mail.MAIL_PORT,
    MAIL_SERVER=settings.mail.MAIL_SERVER,
    MAIL_FROM_NAME=settings.mail.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.mail.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.mail.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.mail.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.mail.VALIDATE_CERTS,
)


mail = FastMail(config=fast_mail_config)


def create_message(recepients: list[str],
                   subject: str,
                   body: str) -> MessageSchema:
    return MessageSchema(
        recipients=recepients,
        subject=subject,
        body=body,
        subtype=MessageType.plain,
    )


async def send_reset_token(user_email: str, reset_token: str) -> None:
    body = (
        f"This is your reset token:\n\n{reset_token}\n\n"
        "Please use it while accessing the following "
        "link to reset your password.\n\n"
        f"{settings.app.host}:{settings.app.port}/auth/reset-password"
    )
    message = create_message(
        recepients=[user_email],
        subject="Async_service_v2 Password Reset.",
        body=body,
    )
    await mail.send_message(message)
