import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.core.utils import get_password_hash
from auth_service.database.schemas import UserResponse, UserCreate, UserLogin, UserChange
from auth_service.database.models import User
from auth_service.database.database import get_db
from auth_service.mail.utils import generate_token_for_email
from auth_service.mail.email_sender import send_confirmation_email

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(background_tasks: BackgroundTasks, user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(or_(User.email == user.email, User.username == user.username)))
    existing_user = existing_user.scalar()
    if existing_user:
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

    hashed_password = get_password_hash(user.password)


    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=False,
        is_admin=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = generate_token_for_email()
    confirmation_url = f"http://localhost:8001/confirm-email?token={token}"
    print(confirmation_url)
    await send_confirmation_email(new_user.email, confirmation_url, background_tasks)

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


@router.post("/logout")
async def logout_user(db: AsyncSession = Depends(get_db)):
    pass


@router.get("/confirm-email")
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    pass

class ChangeUserData:
    @router.post("/change-user-data", response_model=UserChange)
    async def change_user_data(self, db: AsyncSession = Depends(get_db), user: UserChange = Depends(get_password_hash)):
        pass
# понять логику регистрации,
# переписать логин
# написать хранение токена в редисе для почты,
# написать функицю для потверждения емайла,
# написать чендж дата,
# останется jwt токены
