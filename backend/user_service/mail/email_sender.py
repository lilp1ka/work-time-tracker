import os, sys
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from user_service.core.utils import generate_token_for_email
from user_service.core.redis_client import RedisClient

load_dotenv()

MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM = os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"), os.getenv("MAIL_FROM")
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

redis_client = RedisClient()


async def generate_link():
    token = generate_token_for_email()
    confirmation_url = f"http://localhost:8002/team/accept-invite?/token={token}"
    return confirmation_url, token


async def send_invite(email: str):
    confirmation_url, token = await generate_link()

    with open('/user_service/mail/templates/invite_to_team.html') as file:
        html_content = file.read().replace('{{ invitation_link }}', confirmation_url)

    message = MessageSchema(
        subject="Intive to team",
        recipients=[email],
        body=html_content,
        subtype="html"
    )

    print(confirmation_url)
    await redis_client.set_token(email, token, expire=7200)
    await redis_client.close()
    fm = FastMail(conf)
    await fm.send_message(message)
    return confirmation_url, token

