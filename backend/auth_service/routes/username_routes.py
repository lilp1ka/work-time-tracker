import sys
import os
from fastapi import APIRouter, Depends, HTTPException
import jwt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from backend.auth_service.app.jwt_handler import SECRET_KEY, ALGORITHM
from backend.auth_service.core.security import oauth2_scheme

username_router = APIRouter()

@username_router.get("/validate-token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": username}