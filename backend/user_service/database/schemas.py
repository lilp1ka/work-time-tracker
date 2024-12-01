from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    is_active: Optional[bool] = False
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name_group: str
    creator_id: int
    admin_id: int
    type_subscribe: str

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    is_active: Optional[bool] = False

    class Config:
        orm_mode = True
