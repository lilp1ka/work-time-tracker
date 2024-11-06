from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse

from auth_service.mail.utils import generate_token_for_email

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


async def generate_link():
    token = generate_token_for_email()
    confirmation_url = f"http://localhost:8001/confirm-email?token={token}"
    return confirmation_url


async def send_confirmation_email(email: str):
    message = MessageSchema(
        subject="Email Confirmation",
        recipients=[email],
        body=f"Please confirm your email by clicking on the following link: {await generate_link()}",
        subtype="html"
    )
    print(message)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})