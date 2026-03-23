import smtplib
from email.message import EmailMessage

# Данные из вашего примера
MAIL_USERNAME = "Niki"
MAIL_PASSWORD = "tzpx ylmq hdqt cvym"
MAIL_FROM = "nik2000shved@gmail.com"
MAIL_FROM_NAME = "fintex"
MAIL_PORT = 587
MAIL_SERVER = "smtp.gmail.com"
MAIL_STARTTLS = True
MAIL_SSL_TLS = False  # мы используем обычный SMTP с STARTTLS

# Создаем сообщение
msg = EmailMessage()
msg["Subject"] = "Тестовое письмо"
msg["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM}>"
msg["To"] = MAIL_FROM
msg.set_content("Привет! Это тестовое письмо от вашего скрипта.")

# Отправка письма
try:
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        if MAIL_STARTTLS:
            server.starttls()
        server.login(MAIL_FROM, MAIL_PASSWORD)
        server.send_message(msg)
    print("Письмо успешно отправлено!")
except Exception as e:
    print("Ошибка при отправке письма:", e)