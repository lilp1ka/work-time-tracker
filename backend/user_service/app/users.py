from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.database.database import get_db
from user_service.schemas.users_schemas import *

class Users:
    def __init__(self):
        pass

    async def create_user(self, user: UserCreate, db: AsyncSession = Depends(get_db)):
        pass

    @staticmethod
    async def take_username_from_jwt(request: Request):
        return request.state.user.get("username")
