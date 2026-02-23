from dotenv import load_dotenv
import os



class Settings:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance._load()
    return cls._instance
  
  #an other way to do it would be
  #static method: def get_instnace()

  def _load(self):
    self.db_user       = os.getenv("DB_USER")
    self.db_password   = os.getenv("DB_PASSWORD")
    self.db_host       = os.getenv("DB_HOST")
    self.db_port       = os.getenv("DB_PORT")
    self.db_name       = os.getenv("DB_NAME")
    self.database_url  = os.getenv("DATABASE_URL","mysql+aiomysql://user:1234@localhost:3306/biblioteca")
    self.secret_key    = os.getenv("SECRET_KEY")
    self.algorithm     = os.getenv("ALGORITHM")
    self.redis_url     = os.getenv("REDIS_URL")
    self.valid_origins = os.getenv("VALID_ORIGINS", "").split(",")


load_dotenv()

settings = Settings()