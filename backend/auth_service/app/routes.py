import sys
import os
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from auth_service.database.schemas import (
    UserResponse, UserCreate, UserLogin, TokenResponse, TokenRefresh, TokenRefreshResponse
)
from auth_service.database.database import get_db
from auth_service.app.jwt_handler import create_access_token, create_refresh_token, decode_token
from auth_service.database.models import Token

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


@change_router.patch("/change-password")
async def change_password():
    pass


@change_router.patch("/change-email")
async def change_email():
    pass


@change_router.patch("/change-username")
async def change_username():
    pass


@change_router.patch("/reset-password")
async def reset_password():
    pass


@change_router.delete("/delete-user")
async def delete_user():
    pass


@users_router.get("/get-my-user/", response_model=UserResponse)
async def get_my_user(request: Request, db: AsyncSession = Depends(get_db)):
    # {'scope': {'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.4'}, 'http_version': '1.1', 'server': ('172.26.0.4', 8000), 'client': ('172.26.0.1', 46000), 'scheme': 'http', 'method': 'GET', 'root_path': '', 'path': '/users/get-my-user/', 'raw_path': b'/users/get-my-user/', 'query_string': b'', 'headers': [(b'authorization', b'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJzYW1wbG92ZTY2NEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6InNvc2FsMSIsImVtYWlsX2lzX3ZlcmlmaWVkIjpmYWxzZSwiZXhwIjoxNzMxNDQ4MzM1fQ.g20D97VScWkZrSN3iHCgjMMEQmOy_dyScR24WaE6X_k'), (b'user-agent', b'PostmanRuntime/7.37.3'), (b'accept', b'*/*'), (b'postman-token', b'e597f657-74b4-4376-b9cc-896622df5a71'), (b'host', b'127.0.0.1:8001'), (b'accept-encoding', b'gzip, deflate, br'), (b'connection', b'keep-alive')], 'state': {}, 'app': <fastapi.applications.FastAPI object at 0x7be5c9ef9290>, 'starlette.exception_handlers': ({<class 'starlette.exceptions.HTTPException'>: <function http_exception_handler at 0x7be5caf05080>, <class 'starlette.exceptions.WebSocketException'>: <bound method ExceptionMiddleware.websocket_exception of <starlette.middleware.exceptions.ExceptionMiddleware object at 0x7be5c9ee6910>>, <class 'fastapi.exceptions.RequestValidationError'>: <function request_validation_exception_handler at 0x7be5caf1c900>, <class 'fastapi.exceptions.WebSocketRequestValidationError'>: <function websocket_request_validation_exception_handler at 0x7be5caf1dbc0>}, {}), 'router': <fastapi.routing.APIRouter object at 0x7be5cbd71890>, 'endpoint': <function get_my_user at 0x7be5c9b47100>, 'path_params': {}, 'route': APIRoute(path='/users/get-my-user/', name='get_my_user', methods=['GET'])}, '_receive': <bound method RequestResponseCycle.receive of <uvicorn.protocols.http.h11_impl.RequestResponseCycle object at 0x7be5c9727450>>, '_send': <function wrap_app_handling_exceptions.<locals>.wrapped_app.<locals>.sender at 0x7be5c9b75da0>, '_stream_consumed': False, '_is_disconnected': False, '_form': None, '_query_params': QueryParams(''), '_headers': Headers({'authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJzYW1wbG92ZTY2NEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6InNvc2FsMSIsImVtYWlsX2lzX3ZlcmlmaWVkIjpmYWxzZSwiZXhwIjoxNzMxNDQ4MzM1fQ.g20D97VScWkZrSN3iHCgjMMEQmOy_dyScR24WaE6X_k', 'user-agent': 'PostmanRuntime/7.37.3', 'accept': '*/*', 'postman-token': 'e597f657-74b4-4376-b9cc-896622df5a71', 'host': '127.0.0.1:8001', 'accept-encoding': 'gzip, deflate, br', 'connection': 'keep-alive'}), '_cookies': {}}
    from auth_service.app.instances import user_instance
    token = request.headers.get("Authorization")
    payload = decode_token(token)
    user_id = payload.get("id")
    return await user_instance.get_user(user_id, db)

@users_router.get("/get-user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import user_instance
    return await user_instance.get_user(user_id, db)


@users_router.get("/get-all-users", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import user_instance
    return await user_instance.get_all_users(db)


@users_router.get("/get-user-by-username", response_model=UserResponse)
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import user_instance
    return await user_instance.get_user_by_username(username, db)


@users_router.get("/get-user-by-id", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    from auth_service.app.instances import user_instance
    return await user_instance.get_user_by_id(user_id, db)

# разобратся с response_model
