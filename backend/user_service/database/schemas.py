from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = False
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    email_is_verif: bool

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name_group: str
    type_subscribe: str
    is_active: Optional[bool] = False

class TeamCreate(TeamBase):
    creator_id: int
    admin_id: int

class TeamResponse(TeamBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True

class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int

class TeamMemberResponse(TeamMemberBase):
    id: int

    class Config:
        orm_mode = True
