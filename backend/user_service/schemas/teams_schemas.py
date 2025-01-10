from pydantic import BaseModel, EmailStr
from datetime import datetime

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

class RemoveUserFromTeamRequest(BaseModel):
    team_id: int
    user_id: int

class TeamUsersResponse(BaseModel):
    team_id: int
    users: list[int]


class TeamUsersMyListOfTeamsResponse(BaseModel):
    teams: list[int]