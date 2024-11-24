from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from auth_service.app.jwt_handler import SECRET_KEY, ALGORITHM
from auth_service.core.security import oauth2_scheme
from auth_service.core.utils import generate_password
from auth_service.database.models import User
from auth_service.database.database import get_db
from auth_service.mail.email_sender import send_reset_password_email


class UserData:
    def __init__(self):
        pass

    @staticmethod
    async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def get_all_users(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users

    @staticmethod
    async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


    @staticmethod
    async def get_current_user_id(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("id")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return user_id

class ChangeUserData(UserData):
    async def change_password(self, user_id: int, new_password: str, db: AsyncSession = Depends(get_db)):
        user = await self.get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.password = new_password
        db.add(user)
        await db.commit()
        return {"message": "Password updated successfully"}

    async def change_email(self, user_id: int, new_email: EmailStr, db: AsyncSession = Depends(get_db)):
        user = await self.get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.email = new_email
        db.add(user)
        await db.commit()
        return {"message": "Email updated successfully"}

    async def change_username(self, user_id: int, new_username: str, db: AsyncSession = Depends(get_db)):
        user = await self.get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.username = new_username
        db.add(user)
        await db.commit()
        return {"message": "Username updated successfully"}

    async def delete_user(self, user_id: int, db: AsyncSession = Depends(get_db)):
        user = await self.get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        await db.delete(user)
        await db.commit()
        return {"message": "User deleted successfully"}

    async def reset_password(self, user_id: int, db: AsyncSession = Depends(get_db)):
        user = await self.get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        new_password = generate_password()
        print(new_password)
        user.password = new_password
        db.add(user)
        await db.commit()
        await send_reset_password_email(user.email, new_password)
        return {"message": "Password reset successfully"}



user_instance = UserData()
change_user_instance = ChangeUserData()

# get_my_user
# change методы
# написать методы для change через json body и обязательную аутификацию через токен чтобы были example в fastapi docs
# написать тесты для всех методов
# понять как доставать username в других микросервисах с jwt token
# понять как делать запросы к другим микросервисам
