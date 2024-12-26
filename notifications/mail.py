from core.settings import settings


def send_email(email: str, message: str):
    ...


def send_reset_token(email: str, reset_token: str) -> None:
    message = (
        f"This is your reset token:\n\n{reset_token}\n\n"
        "Please use it while accessing the following "
        "link to reset your password.\n\n"
        f"{settings.app.host}:{settings.app.port}/auth/reset-password"
    )
    send_email(email, message)
