from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from core.settings import settings


fast_mail_config = ConnectionConfig(**settings.mail.model_dump())


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
