import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.core.redis_client import RedisClient
from auth_service.core.utils import get_password_hash
from auth_service.database.schemas import UserResponse, UserCreate, UserLogin, UserChange
from auth_service.database.models import User
from auth_service.database.database import get_db
from auth_service.mail.email_sender import send_confirmation_email

router = APIRouter()


class Register:

    def __init__(self):
        self.router = router

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


class Email:
    def __init__(self):
        self.router = router

    @staticmethod
    async def find_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar()

    async def confirm_email(self, email: str, token: str, db: AsyncSession = Depends(get_db)):
        token_from_redis = await redisClient.get_token(email)
        if token_from_redis.decode("utf-8") == token:
            user = await self.find_user_by_email(email, db)
            if user:
                await self.update_verif(user, db)
                await redisClient.delete_token(email)

    @staticmethod
    async def update_verif(user: User, db: AsyncSession = Depends(get_db)):
        if user:
            user.email_is_verified = True
            await db.commit()
            return {"message": f"User {user.email} is now verified"}
        return {"error": "User not found"}


class Login(Email):
    async def login_user(self, email: str, password: str, db: AsyncSession = Depends(get_db)):
        user = await self.find_user_by_email(email, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        if not user.check_password(password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUESTD, detail='Incorrect password')

        return user


class ChangeUserData:
    def __init__(self):
        self.router = router

    async def change_password(self):
        pass

    async def change_email(self):
        pass

    async def change_username(self):
        pass

    async def reset_password(self):
        pass

    @router.post("/change-user-data", response_model=UserChange)
    async def change_user_data(self, db: AsyncSession = Depends(get_db), user: UserChange = Depends(get_password_hash)):
        pass


login_instance = Login()
register_instance = Register()
redisClient = RedisClient()
email_instance = Email()
change_instance = ChangeUserData()


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_instance.register_user(user, db)
    return user


@router.get("/confirm-email")
async def confirm_email(token: str, email: str, db: AsyncSession = Depends(get_db)):
    await email_instance.confirm_email(email, token, db)
    return {"message": "Email confirmation successful"}


@router.post("/login", response_model=UserResponse)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await login_instance.login_user(user.email, user.password, db)
    return user

# change_data
# jwt
# logout
# разобратся с response_model
