import sys
import os

from auth_service.database.schemas import UserResponse, UserCreate, UserLogin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.database.database import get_db

auth_router = APIRouter()
email_router = APIRouter()
users_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import register_instance
    user = await register_instance.register_user(user, db)
    return user


@auth_router.post("/login", response_model=UserResponse)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import login_instance
    user = await login_instance.login_user(user.email, user.password, db)
    return user


@email_router.get("/confirm-email")
async def confirm_email(token: str, email: str, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import email_instance
    return await email_instance.confirm_email(email, token, db)