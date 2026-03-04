from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv


DATABASE_URL = os.getenv("DATABASE_URL", "")



engine = create_async_engine(
  url=DATABASE_URL,
  pool_pre_ping=True,
  echo=True
)


SessionLocal = async_sessionmaker(
  engine,
  class_=AsyncSession,
  expire_on_commit=False,
  autocommit=False,
  autoflush=False,
)