from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from backend.user_service.app.teams import create_team, get_team, update_team, delete_team, add_team_member, \
    get_team_members, remove_team_member
from backend.user_service.database.schemas import TeamCreate, TeamResponse, TeamMemberResponse, UserCreate
from backend.user_service.database.database import get_db

team_router = APIRouter()

@team_router.post("/teams", response_model=TeamResponse)
async def create_team_endpoint(team: TeamCreate, db: AsyncSession = Depends(get_db)):
    return await create_team(db, team)

@team_router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team_endpoint(team_id: int, db: AsyncSession = Depends(get_db)):
    team = get_team(db, team_id)
    return team

@team_router.put("/teams/{team_id}", response_model=TeamResponse)
async def update_team_endpoint(team_id: int, db: AsyncSession = Depends(get_db)):
    team = update_team(db, team_id)
    return team

@team_router.delete("/teams/{team_id}", response_model=TeamResponse)
async def delete_team_endpoint(team_id: int, db: AsyncSession = Depends(get_db)):
    await delete_team(db, team_id)



@team_router.post("/teams/{team_id}/members", response_model=TeamMemberResponse)
async def add_member(team_id: int, data: UserCreate, db: AsyncSession = Depends(get_db)):
    member = await add_team_member(db, team_id, data.username)
    return member

@team_router.get("/teams/{team_id}/members", response_model=List[TeamMemberResponse])
async def get_members(team_id: int, db: AsyncSession = Depends(get_db)):
    members = await get_team_members(db, team_id)
    return members

@team_router.delete("/teams/{team_id}/members/{username}", response_model=TeamMemberResponse)
async def delete_member(team_id: int, username: str, db: AsyncSession = Depends(get_db)):
    await remove_team_member(db, team_id, username)
