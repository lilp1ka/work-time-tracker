from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth_service.app.jwt_handler import decode_token
from auth_service.database.database import get_db
from auth_service.database.schemas import UserResponse
from auth_service.app.user_data import user_instance

users_router = APIRouter()


@users_router.get("/get-my-user/", response_model=UserResponse)
async def get_my_user():
    pass


@users_router.get("/get-user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_instance.get_user(user_id, db)


@users_router.get("/get-all-users", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_instance.get_all_users(db)


@users_router.get("/get-user-by-username", response_model=UserResponse)
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    return await user_instance.get_user_by_username(username, db)


@users_router.get("/get-user-by-id", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_instance.get_user_by_id(user_id, db)
