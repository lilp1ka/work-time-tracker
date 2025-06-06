from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth_service.core.redis_client import redisClient
from auth_service.database.models import User
from auth_service.database.database import get_db

class Email:
    def __init__(self):
        pass

    async def confirm_email(self, email: str, token: str, db: AsyncSession = Depends(get_db)):
        if email is None or token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email or token not provided')

        if not await redisClient.key_exists(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token not found for this email')

        token_from_redis = await redisClient.get_token(email)
        if token_from_redis.decode("utf-8") != token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='token not valid')

        await redisClient.delete_token(email)
        return {f"user successfully invited"}


email_instance = Email()