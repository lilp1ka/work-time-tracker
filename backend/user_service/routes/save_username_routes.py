from fastapi import Depends, HTTPException, Header, APIRouter
from httpx import AsyncClient
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from backend.user_service.app.users import create_user
from backend.user_service.database.database import get_db

save_username_router = APIRouter
AUTH_SERVICE_URL = "http://auth_service:8000/validate-token"


@save_username_router.post("/save-username")
async def save_username(authorization: str = Header(...), db=Depends(get_db)):
    async with AsyncClient() as client:
        response = await client.get(AUTH_SERVICE_URL, headers={"Authorization": authorization})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Invalid token")

        username = response.json().get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username not found in token")

        await create_user(db, username=username)
        return {"message": "Username saved successfully", "username": username}