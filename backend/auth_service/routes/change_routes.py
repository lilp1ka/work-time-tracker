from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.database.schemas import ChangePasswordRequest, ChangeEmailRequest, ChangeUsernameRequest, DeleteUserRequest
from auth_service.app.user_data import change_user_instance, user_instance
from auth_service.database.database import get_db
from auth_service.core.security import oauth2_scheme

change_router = APIRouter()

@change_router.patch("/change-password")
async def change_password(data: ChangePasswordRequest, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = await user_instance.get_current_user_id(token)
    return await change_user_instance.change_password(user_id, data.new_password, db)

@change_router.patch("/change-email")
async def change_email(data: ChangeEmailRequest, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = await user_instance.get_current_user_id(token)
    return await change_user_instance.change_email(user_id, data.new_email, db)

@change_router.patch("/change-username")
async def change_username(data: ChangeUsernameRequest, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = await user_instance.get_current_user_id(token)
    return await change_user_instance.change_username(user_id, data.new_username, db)

@change_router.patch("/reset-password")
async def reset_password(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = await user_instance.get_current_user_id(token)
    return await change_user_instance.reset_password(user_id, db)

@change_router.delete("/delete-user")
async def delete_user(data: DeleteUserRequest, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = await user_instance.get_current_user_id(token)
    return await change_user_instance.delete_user(user_id, db)