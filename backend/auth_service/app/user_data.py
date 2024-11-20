from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth_service.database.models import User
from auth_service.database.database import get_db


class ChangeUserData:
    def __init__(self):
        pass

    async def change_password(self):
        pass

    async def change_email(self):
        pass

    async def change_username(self):
        pass

    async def reset_password(self):
        pass

    async def delete_user(self):
        pass


class UserData:
    def __init__(self):
        pass
    @staticmethod
    async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def get_all_users(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users

    @staticmethod
    async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

user_instance = UserData()
change_user_instance = ChangeUserData()