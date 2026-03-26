import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+aiomysql://user:1234@db:3306/biblioteca"
)


engine = create_async_engine(url=DATABASE_URL, pool_pre_ping=True, echo=True)


SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
