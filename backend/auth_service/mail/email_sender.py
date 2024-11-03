from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="axomjak@gmail.com",
    MAIL_PASSWORD="dmzs rnhi zidk sywg",
    MAIL_FROM="axomjak@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_confirmation_email(email: str, token: str, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject="Email Confirmation",
        recipients=[email],
        body=f"Please confirm your email by clicking on the following link: http://localhost:8000/auth/confirm-email?token={token}",
        subtype="html"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)