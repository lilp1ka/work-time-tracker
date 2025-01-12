from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.database.database import get_db
from user_service.schemas.users_schemas import *
from user_service.app.users import users

users_router = APIRouter()

@users_router.post("/create_user", response_model=UserResponse)
async def create_user(request: Request, db: AsyncSession = Depends(get_db)):
    user = await users.create_user(request, db)
    return user

@users_router.patch("/change_username", response_model=UserResponse)
async def change_username(request: Request, user: ChangeUsernameRequest, db: AsyncSession = Depends(get_db)):
    user = await users.change_username(request, user, db)
    return user

@users_router.delete("/delete_user")
async def delete_user(request: Request, db: AsyncSession = Depends(get_db)):
    user = await users.delete_user(request, db)
    return user

@users_router.get("/user_info", response_model=UserResponse)
async def user_info(request: Request, db: AsyncSession = Depends(get_db)):
    user = await users.get_info(request, db)
    return user

