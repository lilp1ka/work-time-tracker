import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import HTTPException, Depends, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.core.utils import get_password_hash
from auth_service.database.schemas import UserCreate
from auth_service.database.models import User
from auth_service.database.database import get_db
from auth_service.mail.email_sender import send_confirmation_email



class Register:

    def __init__(self):
        pass

    @staticmethod
    async def is_user_exists(db: AsyncSession, user: UserCreate) -> User:
        result = await db.execute(select(User).where(or_(User.email == user.email, User.username == user.username)))
        return result.scalar()

    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        new_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def register_user(self, user: UserCreate, db: AsyncSession = Depends(get_db)):
        existing_user = await self.is_user_exists(db, user)

        if existing_user:
            if existing_user.email == user.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
            if existing_user.username == user.username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already registered')
        new_user = await self.create_user(db, user)
        await send_confirmation_email(new_user.email)
        return new_user


class Login:
    @staticmethod
    async def login_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
        from auth_service.app.email_logic import email_instance
        user = await email_instance.find_user_by_email(email, db)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if not user.check_password(password):
            raise HTTPException(status_code=400, detail='Incorrect password')

        return user


login_instance = Login()
register_instance = Register()
