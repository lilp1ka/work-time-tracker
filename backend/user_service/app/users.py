import sys, os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from backend.user_service.database.models import User
from backend.user_service.database.schemas import UserCreate

async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise ValueError("User with this email or username already exists")
    return new_user

# async def get_user(db: AsyncSession, user_id: int) -> User:
    # result = await db.execute(select(User).where(User.id == user_id))
    # user = result.scalars().first()
    # return user


async def get_user(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    return user


async def update_user(db: AsyncSession, username: str, updates: dict) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return None
    for key, value in updates.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, username: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True


