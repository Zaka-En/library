from sqlalchemy.orm import declarative_base
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


engine = create_async_engine(
  url=settings.database_url,
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

Base = declarative_base()

async def get_db_session():
  async with SessionLocal() as session:
    yield session
  