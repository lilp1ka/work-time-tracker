from passlib.context import CryptContext
from uuid import uuid4
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def generate_token_for_email() -> str:
    return str(uuid4())
