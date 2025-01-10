from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://root:root@user-db:5432/user_db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
