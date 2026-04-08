from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# 1. Конфигурация почты (встроена напрямую)
conf = ConnectionConfig(
    MAIL_USERNAME="nik2000shved@gmail.com",
    MAIL_PASSWORD="tzpx ylmq hdqt cvym",
    MAIL_FROM="nik2000shved@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="fintex",  # Имя отправителя
    MAIL_STARTTLS=True,  # True для Gmail
    MAIL_SSL_TLS=False,  # False для Gmail
    USE_CREDENTIALS=True,  # Обязательно!
    VALIDATE_CERTS=True,  # Проверка сертификатов
)

# 2. Создаем объект FastMail (один раз)
fm = FastMail(conf)


async def send_verification_email(email: str, verify_link: str):
    """
    Отправляет письмо для подтверждения email
    """
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

    message = MessageSchema(
        subject="Подтверждение email | Fintex",
        recipients=[email],  # Список получателей
        body=html_body,
        subtype="html",  # HTML письмо
    )

    try:
        await fm.send_message(message)
        print(f"Verification email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


# 3. Пример использования (для теста)
if __name__ == "__main__":
    import asyncio

    test_email = "nik2000shved@gmail.com"
    test_link = "https://example.com/verify?token=12345"
    asyncio.run(send_verification_email(test_email, test_link))
