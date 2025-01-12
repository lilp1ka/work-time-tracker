from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.database.database import get_db
from user_service.database.models import Team, TeamMember
from user_service.schemas.teams_schemas import *
from user_service.mail.email_sender import send_invite
from user_service.core.redis_client import redisClient
from user_service.core.utils import generate_token_for_email


class Teams:
    def __init__(self):
        pass

    async def create_team(self,request: Request, team: TeamCreate, db: AsyncSession = Depends(get_db)):
        existing_team = await db.execute(select(Team).where(Team.name_group == team.name))

        existing_team = existing_team.scalar()
        if existing_team:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team with this name already exists")
        creator_id = await self.take_id_from_jwt(request)
        new_team = Team(
            name_group=team.name,
            creator_id=creator_id,
            is_active=False
        )
        db.add(new_team)
        await db.commit()
        await db.refresh(new_team)
        team_member = TeamMember(team_id=new_team.id, user_id=creator_id)
        db.add(team_member)
        await db.commit()
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
    async def add_user_to_team(self, request: Request, team: Optional[AddUserToTeamRequest] = None,
                               db: AsyncSession = Depends(get_db)):
        if team is None:
            token = request.query_params.get("token")
            team_id = request.query_params.get("team_id")
            try:
                team_id = int(team_id)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Invalid team_id format")

            user_id = request.state.user_id

            team_data = await db.execute(select(Team).where(Team.id == team_id))
            if not team_data.scalar():
                raise HTTPException(status_code=404, detail="Team not found")

            existing_member = await db.execute(
                select(TeamMember).where(TeamMember.team_id == team_id).where(TeamMember.user_id == user_id)
            )
            if existing_member.scalar():
                raise HTTPException(status_code=400, detail="User is already a member of the team")

            new_member = TeamMember(team_id=team_id, user_id=user_id)
            db.add(new_member)
            await db.commit()

            return {"message": "User successfully added to the team"}

        email = team.email
        team_id = team.team_id
        if email:
            await redisClient.get_token(email)
            confirmation_url, token = await send_invite(email)
        else:
            token = generate_token_for_email()
            await redisClient.set_token(f"team:{team_id}", token, expire=7200)
            confirmation_url = f"http://localhost:8002/team/accept-invite?/token={token}&team_id={team_id}"

        users = await self.get_team_users(team_id, db)

        response = {
            "team_id": team_id,
            "users": users["users"],
            "confirmation_url": confirmation_url
        }
        return response

    async def get_team_users(self, team_id: int, db: AsyncSession):
        team_data = await db.execute(select(Team).where(Team.id == team_id))
        team_data = team_data.scalar()
        if not team_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

        team_members = await db.execute(
            select(TeamMember.user_id).where(TeamMember.team_id == team_id)
        )
        team_members = team_members.scalars().all()

        return {
            "team_id": team_id,
            "creator_id": team_data.creator_id,
            "users": team_members
        }

    async def remove_user_from_team(self, request: Request, team: RemoveUserFromTeamRequest,
                                    db: AsyncSession = Depends(get_db)):
        user_id = await self.take_id_from_jwt(request)

        team_data = await db.execute(select(Team).where(Team.id == team.team_id))
        team_data = team_data.scalar()
        if not team_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

        if team_data.creator_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the creator of this team")

        existing_member = await db.execute(
            select(TeamMember).where(TeamMember.team_id == team.team_id).where(TeamMember.user_id == team.user_id))
        existing_member = existing_member.scalar()
        if not existing_member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the team")

        await db.delete(existing_member)
        await db.commit()

        return {"message": f"User with ID {team.user_id} successfully removed from team"}

    async def get_team_info(self, team_id: int, db: AsyncSession = Depends(get_db)):
        team = await db.execute(select(Team).where(Team.id == team_id))
        team = team.scalar()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        return team

    async def my_teams(self, request: Request, db: AsyncSession = Depends(get_db)):
        # Получаем user_id из JWT токена (авторизованный пользователь)
        user_id = await self.take_id_from_jwt(request)

        # Выполняем запрос для получения всех team_id, где user_id является участником
        teams_query = await db.execute(
            select(Team).join(TeamMember).where(TeamMember.user_id == user_id)
        )

        # Получаем список команд, в которых состоит пользователь
        teams = teams_query.scalars().all()

        # Преобразуем команды в нужный формат
        result = [{"team_id": team.id, "name": team.name_group} for team in teams]

        # Возвращаем список команд
        return {"teams": result}

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
