import sys, os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from backend.user_service.database.models import Team, TeamMember
from backend.user_service.database.schemas import TeamCreate, TeamMemberBase

async def create_team(db: AsyncSession, team: TeamCreate):
    new_team = Team(
        name_group=team.name_group,
        creator_id=team.creator_id,
        admin_id=team.admin_id,
        type_subscribe=team.type_subscribe,
        is_active=team.is_active,
    )
    db.add(new_team)
    try:
        await db.commit()
        await db.refresh(new_team)
    except IntegrityError:
        await db.rollback()
        raise ValueError("User with this email or username already exists")
    return new_team

async def get_team(db: AsyncSession, team_id: int) -> Team:
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalars().first()
    return team

async def update_team(db: AsyncSession, team_id: int, updates: dict) -> Team:
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalars().first()
    if not team:
        return None
    for key, value in updates.items():
        setattr(team, key, value)
    await db.commit()
    await db.refresh(team)
    return team

async def delete_team(db: AsyncSession, team_id: int) -> bool:
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalars().first()
    if not team:
        return False
    await db.delete(team)
    await db.commit()
    return True



async def add_team_member(db: AsyncSession, team_id: int, user_id: int) -> TeamMember:
    new_member = TeamMember(team_id=team_id, user_id=user_id)
    db.add(new_member)
    try:
        await db.commit()
        await db.refresh(new_member)
        return new_member
    except IntegrityError:
        await db.rollback()
        return None

async def get_team_members(db: AsyncSession, team_id: int) -> list[TeamMember]:
    result = await db.execute(select(TeamMember).where(TeamMember.team_id == team_id))
    return result.scalars().all()

async def remove_team_member(db: AsyncSession, team_id: int, user_id: int) -> bool:
    result = await db.execute(select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user_id))
    member = result.scalars().first()
    if not member:
        return False

    await db.delete(member)
    await db.commit()
    return True

