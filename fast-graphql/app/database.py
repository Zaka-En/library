from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

DB_URL = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(
  DB_URL,
  pool_pre_ping=True,
  echo=True
)


# Session
SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)


Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
