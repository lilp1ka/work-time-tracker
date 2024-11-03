from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.schemas import UserCreate, UserResponse, UserLogin
from database.models import User
from database.database import get_db
from core.utils import get_password_hash, generate_token_for_email


router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.email == user.email))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=UserResponse)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.email == user.email))
    db_user = existing_user.scalar()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")

    if not db_user.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    return db_user