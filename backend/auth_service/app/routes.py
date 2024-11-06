import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.core.redis_client import RedisClient
from auth_service.core.utils import get_password_hash
from auth_service.database.schemas import UserResponse, UserCreate, UserLogin, UserChange, EmailConfirm
from auth_service.database.models import User
from auth_service.database.database import get_db
from auth_service.mail.email_sender import send_confirmation_email

router = APIRouter()


class Register:

    def __init__(self):
        self.router = router

    async def is_user_exists(self, db: AsyncSession, user: UserCreate) -> User:
        result = await db.execute(select(User).where(or_(User.email == user.email, User.username == user.username)))
        return result.scalar()

    async def create_user(self, db: AsyncSession, user: UserCreate) -> User:
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

    async def find_user_by_email(self, email: str, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar()

    async def confirm_email(self, token: str, email: str, db: AsyncSession = Depends(get_db)):
        token_from_redis = await redisClient.get_token(email)
        if token_from_redis.decode("utf-8") == token:
            user = await self.find_user_by_email(email, db)
            if user:
                await self.update_verif(user, db)
                await redisClient.delete_token(email)

    async def update_verif(self, user: User, db: AsyncSession = Depends(get_db)):
        if user:
            user.email_is_verified = True
            await db.commit()
            return {"message": f"User {user.email} is now verified"}
        return {"error": "User not found"}



register_instance = Register()
redisClient = RedisClient()
email_instance = Email()


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
    existing_user = await db.execute(select(User).where(User.email == user.email))
    db_user = existing_user.scalar()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")

    if not db_user.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    return db_user


@router.post("/logout")
async def logout_user(db: AsyncSession = Depends(get_db)):
    pass


class ChangeUserData:
    @router.post("/change-user-data", response_model=UserChange)
    async def change_user_data(self, db: AsyncSession = Depends(get_db), user: UserChange = Depends(get_password_hash)):
        pass
# понять логику регистрации, +
# переписать логин +
# написать хранение токена в редисе для почты, +
# написать функицю для потверждения емайла, +
# написать чендж дата,
# останется jwt токены
