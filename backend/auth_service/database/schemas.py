from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class ChangeUserData(BaseModel):
    password: str
    email: EmailStr
    username: str
    reset_password: str
    delete_user: str

class UserData(BaseModel):
    get_user: str
    get_all_users: str
    get_user_by_username: str
    get_user_by_id: str

