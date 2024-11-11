import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.database.schemas import (
    UserResponse, UserCreate, UserLogin, TokenResponse, TokenRefresh, TokenRefreshResponse
)
from auth_service.database.database import get_db
from auth_service.app.jwt_handler import create_access_token, create_refresh_token, decode_token
from auth_service.database.models import Token

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

auth_router = APIRouter()
email_router = APIRouter()
users_router = APIRouter()
token_router = APIRouter()
change_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import register_instance
    user = await register_instance.register_user(user, db)
    return user


@auth_router.post("/login", response_model=TokenResponse)
async def login_user(user: UserLogin, request: Request, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import login_instance
    user = await login_instance.login_user(user.email, user.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"id": user.id, "email": user.email, "username": user.username,
                                             "email_is_verified": user.email_is_verified})
    refresh_token = create_refresh_token(data={"id": user.id, "email": user.email, "username": user.username,
                                               "email_is_verified": user.email_is_verified})

    device_info = request.headers.get("User-Agent")

    existing_token = await db.execute(
        select(Token).filter(Token.user_id == user.id, Token.device_info == device_info)
    )
    existing_token = existing_token.scalar()

    if existing_token:
        existing_token.refresh_token = refresh_token
        existing_token.expires_at = datetime.utcnow() + timedelta(days=7)
    else:
        token = Token(
            user_id=user.id,
            device_info=device_info,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db.add(token)

    await db.commit()

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60,
        refresh_token=refresh_token
    )


@token_router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(token_data: TokenRefresh, request: Request, db: AsyncSession = Depends(get_db)):
    payload = decode_token(token_data.refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token. Payload not found")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token. User id not found")

    device_info = request.headers.get("User-Agent")
    token = await db.execute(
        select(Token).filter(Token.refresh_token == token_data.refresh_token, Token.device_info == device_info))
    token = token.scalar()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token. Token not found")

    access_token = create_access_token(
        data={"id": user_id, "email": payload.get("email"), "username": payload.get("username"),
              "email_is_verified": payload.get("email_is_verified")})

    return TokenRefreshResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60
    )


@auth_router.post("/logout")
async def logout(request: Request, db: AsyncSession = Depends(get_db)):
    device_info = request.headers.get("User-Agent")
    token = await db.execute(select(Token).filter(Token.device_info == device_info))
    token = token.scalar()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token. Token not found")

    await db.delete(token)
    await db.commit()
    return {"message": "Logout successful"}


@email_router.get("/confirm-email")
async def confirm_email(token: str, email: str, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import email_instance
    return await email_instance.confirm_email(email, token, db)

@change_router.post("/change-password")
async def change_password():
    pass

@change_router.post("/change-email")
async def change_email():
    pass

@change_router.post("/change-username")
async def change_username():
    pass

@change_router.post("/reset-password")
async def reset_password():
    pass

@change_router.post("/delete-user")
async def delete_user():
    pass

@users_router.get("/get-user")
async def get_user():
    pass

@users_router.get("/get-all-users")
async def get_all_users():
    pass

@users_router.get("/get-user-by-username")
async def get_user_by_username():
    pass

@users_router.get("/get-user-by-id")
async def get_user_by_id():
    pass




# разобратся с response_model
