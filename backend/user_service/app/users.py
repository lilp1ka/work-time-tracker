from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.database.database import get_db
from user_service.database.models import User
from user_service.schemas.users_schemas import *

class Users:
    def __init__(self):
        pass

    async def create_user(self, request: Request, db: AsyncSession = Depends(get_db)):
        username = await self.take_username_from_jwt(request)
        existing_user = await self.is_user_exists(db, username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registered')

        new_user = User(
            username=username,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def change_username(self, request: Request, user: ChangeUsernameRequest, db: AsyncSession = Depends(get_db)):
        old_username = await self.take_username_from_jwt(request)
        print(old_username)
        print(old_username)
        print(old_username)
        existing_user = await db.execute(select(User).where(User.username == old_username))
        existing_user = existing_user.scalar()
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if await self.is_user_exists(db, user.new_username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        existing_user.username = user.new_username
        await db.commit()
        await db.refresh(existing_user)

        return existing_user

    async def delete_user(self, request: Request, db: AsyncSession = Depends(get_db)):
        username = await self.take_username_from_jwt(request)

        user = await db.execute(select(User).where(User.username == username))
        user = user.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await db.delete(user)
        await db.commit()
        return {"message": "User deleted successfully"}

    async def get_info(self, request: Request, db: AsyncSession = Depends(get_db)):
        username = await self.take_username_from_jwt(request)

        user = await db.execute(select(User).where(User.username == username))
        user = user.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def take_username_from_jwt(request: Request):
        return request.state.user

    @staticmethod
    async def is_user_exists(db: AsyncSession, username: str) -> User:
        result = await db.execute(select(User.id, User.username, User.is_active).where(User.username == username))
        return result.scalar()

users = Users()