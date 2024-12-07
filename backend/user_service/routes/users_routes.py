from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from backend.user_service.app.users import create_user, get_user, update_user, delete_user
from backend.user_service.database.schemas import UserCreate, UserResponse
from backend.user_service.database.database import get_db

user_router = APIRouter()


@user_router.post("/users", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@user_router.get("/users/{username}", response_model=UserResponse)
async def get_user_endpoint(username: str, db: AsyncSession = Depends(get_db)):
    user = get_user(db, username)
    return user

@user_router.put("/users/{username}", response_model=UserResponse)
async def update_user_endpoint(username: str, updates: dict, db: AsyncSession = Depends(get_db)):
    user = update_user(db, username, updates)
    return user

@user_router.delete("/users/{username}")
async def delete_user_endpoint(username: str, db: AsyncSession = Depends(get_db)):
    await delete_user(db, username)
