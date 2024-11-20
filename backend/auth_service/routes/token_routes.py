from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.requests import Request
from sqlalchemy import select
from auth_service.database.schemas import TokenRefresh, TokenRefreshResponse
from auth_service.database.database import get_db
from auth_service.app.jwt_handler import decode_token, create_access_token
from auth_service.database.models import Token

token_router = APIRouter()

@token_router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(token_data: TokenRefresh, request: Request, db: AsyncSession = Depends(get_db)):
    access_token = request.headers.get("Authorization")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not provided")

    access_payload = decode_token(access_token)
    if not access_payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    refresh_payload = decode_token(token_data.refresh_token)
    if not refresh_payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token. Payload not found")

    user_id = refresh_payload.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token. User id not found")

    if access_payload.get("id") != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token and refresh token do not match")

    device_info = request.headers.get("User-Agent")
    token = await db.execute(
        select(Token).filter(Token.refresh_token == token_data.refresh_token, Token.device_info == device_info)
    )
    token = token.scalar()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token. Token not found")

    new_access_token = create_access_token(
        data={"id": user_id, "email": refresh_payload.get("email"), "username": refresh_payload.get("username"),
              "email_is_verified": refresh_payload.get("email_is_verified")}
    )

    return (TokenRefreshResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=30 * 60
    ))