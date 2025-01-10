from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class TeamCreate(BaseModel):
    name: str

class TeamResponse(BaseModel):
    id: int
    name_group: str
    created_at: datetime
    creator_id: int

    class Config:
        from_attributes = True

class ChangeTeamNameRequest(BaseModel):
    team_id: int
    new_name: str

class DeleteTeamRequest(BaseModel):
    team_id: int


class AddUserToTeamRequest(BaseModel):
    team_id: int
    email: Optional[str] = None

class TeamUsersResponse(BaseModel):
    team_id: int
    users: list[int]
    confirmation_url: Optional[str] = None

class TeamUsersListResponse(BaseModel):
    team_id: int
    creator_id: int
    users: list[int]

class RemoveUserFromTeamRequest(BaseModel):
    team_id: int
    user_id: int

class TeamInfo(BaseModel):
    team_id: int
    name: str

class TeamUsersMyListOfTeamsResponse(BaseModel):
    teams: list[TeamInfo]