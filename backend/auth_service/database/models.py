from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from passlib.context import CryptContext

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    email_is_verified = Column(Boolean, default=False)


    def check_password(self, password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.hashed_password)


class Token(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    device_info = Column(String(255))
    refresh_token = Column(String(512), nullable=False)
    issued_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    expires_at = Column(TIMESTAMP, nullable=False)
    valid = Column(Boolean, default=True)
