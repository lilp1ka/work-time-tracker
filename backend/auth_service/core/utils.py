from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from uuid import uuid4


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_token_for_email() -> str:
    return str(uuid4())
