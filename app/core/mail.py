from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,  # Имя отправителя
    MAIL_STARTTLS=settings.MAIL_STARTTLS,  # True для Gmail
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,  # False для Gmail
    USE_CREDENTIALS=True,  # Обязательно!
    VALIDATE_CERTS=True,  # Проверка сертификатов
)

# 2. СОЗДАЕМ ОБЪЕКТ FastMail (ОДИН РАЗ)
fm = FastMail(conf)


async def send_verification_email(email: str, verify_link: str):
    """
    Отправляет письмо для подтверждения email
    """
    # Создаем HTML-письмо (можно красиво оформить)
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Подтверждение email</title>
    </head>
    <body>
        <h2>Подтверждение регистрации</h2>
        <p>Здравствуйте!</p>
        <p>Для подтверждения вашего email перейдите по ссылке:</p>
        <p><a href="{verify_link}">Подтвердить email</a></p>
        <p>Если ссылка не работает, скопируйте в браузер:</p>
        <p>{verify_link}</p>
        <p>Ссылка действительна 24 часа.</p>
        <hr>
        <p>Если вы не регистрировались, просто проигнорируйте это письмо.</p>
    </body>
    </html>
    """

    # Создаем сообщение
    message = MessageSchema(
        subject="Подтверждение email | Your App Name",
        recipients=[email],  # Всегда список, даже для одного получателя
        body=html_body,
        subtype="html",  # Указываем, что это HTML
    )

    try:
        # Отправляем письмо
        await fm.send_message(message)
        print(f"Verification email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
