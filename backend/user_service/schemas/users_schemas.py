from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class ChangeUsernameRequest(BaseModel):
    new_username: str

