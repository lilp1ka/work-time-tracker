from fastapi import APIRouter, Depends, HTTPException, status, Request
from user_service.app.teams import teams, team_user
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.schemas.teams_schemas import *
from user_service.database.database import get_db


teams_user_router = APIRouter()
teams_router = APIRouter()

@teams_router.post("/create_team", response_model=TeamResponse)
async def create_team(team: TeamCreate, db: AsyncSession = Depends(get_db)):
    team = await teams.create_team(team, db)
    return team

@teams_router.patch("/change_team_name", response_model=TeamResponse)
async def change_team_name(team: ChangeTeamNameRequest, db: AsyncSession = Depends(get_db)):
    team = await teams.change_team_name(team, db)
    return team

@teams_router.delete("/delete_team")
async def delete_team(team: DeleteTeamRequest, db: AsyncSession = Depends(get_db)):
    team = await teams.delete_team(team, db)
    return team

@teams_router.get("/team_info", response_model=TeamResponse)
async def team_info(team_id: int, db: AsyncSession = Depends(get_db)):
    team = await teams.team_info(team_id, db)
    return team

@teams_user_router.post("/add_user_to_team", response_model=TeamUsersResponse)
async def add_user_to_team(request: Request, team: AddUserToTeamRequest, db: AsyncSession = Depends(get_db)):
    team = await team_user.add_user_to_team(request, team, db)
    return team

@teams_user_router.delete("/remove_user_from_team")
async def remove_user_from_team(request: Request, team: RemoveUserFromTeamRequest, db: AsyncSession = Depends(get_db)):
    team = await team_user.remove_user_from_team(request, team, db)
    return team

@teams_user_router.get("/team_users", response_model=TeamUsersResponse)
async def team_users(team_id: int, db: AsyncSession = Depends(get_db)):
    team = await teams.get_team_users(team_id, db)
    return team

@teams_user_router.get("/my_teams", response_model=TeamUsersMyListOfTeamsResponse)
async def get_my_teams(request: Request, db: AsyncSession = Depends(get_db)):
    teams = await team_user.get_my_teams(request, db)
    return teams