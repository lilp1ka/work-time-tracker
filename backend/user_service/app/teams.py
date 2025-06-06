from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.database.database import get_db
from user_service.database.models import Team, TeamMember
from user_service.schemas.teams_schemas import *
from user_service.mail.email_sender import send_invite


class Teams:
    def __init__(self):
        pass

    async def create_team(self,request: Request, team: TeamCreate, db: AsyncSession = Depends(get_db)):
        new_team = Team(
            name_group=team.name,
            creator_id=await self.take_id_from_jwt(request),
            is_active=False
        )
        db.add(new_team)
        await db.commit()
        await db.refresh(new_team)
        return new_team

    async def change_team_name(self, team: ChangeTeamNameRequest, db: AsyncSession = Depends(get_db)):
        existing_team = await db.execute(select(Team).where(Team.id == team.team_id))
        existing_team = existing_team.scalar()
        if not existing_team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

        existing_team.name_group = team.new_name
        await db.commit()
        await db.refresh(existing_team)

        return existing_team

    async def delete_team(self, team: DeleteTeamRequest, db: AsyncSession = Depends(get_db)):
        existing_team = await db.execute(select(Team).where(Team.id == team.team_id))
        existing_team = existing_team.scalar()
        if not existing_team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        await db.delete(existing_team)
        await db.commit()
        return {"message": "Team deleted successfully"}

    @staticmethod
    async def take_id_from_jwt(request: Request):
        return request.state.user_id

class TeamUser(Teams):
    async def add_user_to_team_email(self, request: Request, team: AddUserToTeamRequest,
                                     db: AsyncSession = Depends(get_db)):
        email = team.email
        confirmation_url, token = await send_invite(email)

        team_id = team.team_id
        users = await self.get_team_users(team_id, db)

        return {"team_id": team_id, "users": users["users"], "message": "Invite link has been sent",
                "confirmation_url": confirmation_url}

    async def get_team_users(self, team_id: int, db: AsyncSession):
        result = await db.execute(select(TeamMember.user_id).where(TeamMember.team_id == team_id))
        users = result.scalars().all()
        return {"team_id": team_id, "users": users}

    async def remove_user_from_team(self, request: Request, team: RemoveUserFromTeamRequest,
                                    db: AsyncSession = Depends(get_db)):
        user_id = await self.take_user_id_from_jwt(request)
        existing_member = await db.execute(
            select(TeamMember).where(TeamMember.team_id == team.team_id).where(TeamMember.user_id == user_id))
        existing_member = existing_member.scalar()
        if not existing_member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in team")
        await db.delete(existing_member)
        await db.commit()
        return {"message": "User removed from team successfully"}

    async def get_team_info(self, team_id: int, db: AsyncSession = Depends(get_db)):
        team = await db.execute(select(Team).where(Team.id == team_id))
        team = team.scalar()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        return team

    async def my_teams(self, db: AsyncSession = Depends(get_db)):
        user_id = await self.take_user_id_from_jwt(request)
        teams = await db.execute(select(TeamMember.team_id).where(TeamMember.user_id == user_id))
        teams = teams.scalars().all()
        return {"teams": teams}

    @staticmethod
    async def take_user_id_from_jwt(request: Request):
        return request.state.user

    @staticmethod
    async def is_user_exists(db: AsyncSession, user_id: int):
        result = await db.execute(select(TeamMember).where(TeamMember.user_id == user_id))
        return result.scalar()

    @staticmethod
    async def is_team_exists(db: AsyncSession, team_id: int):
        result = await db.execute(select(Team).where(Team.id == team_id))
        return result.scalar()

    @staticmethod
    async def is_user_in_team(db: AsyncSession, team_id: int, user_id: int):
        result = await db.execute(
            select(TeamMember).where(TeamMember.team_id == team_id).where(TeamMember.user_id == user_id))
        return result.scalar()

teams = Teams()
team_user = TeamUser()
