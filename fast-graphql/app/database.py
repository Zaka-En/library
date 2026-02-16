from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

DB_URL = f"mysql+aiomysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(
  DB_URL,
  pool_pre_ping=True,
  echo=True
)


# Session async
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
  