from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from app.schema.inputs import RegisterInput, LoginInput
from app.models.user import User
from app.utils.auth import create_access_token
from datetime import timedelta
from typing import Tuple

REFRESH_TOKEN_EXPIRY=120 #6 months

class UserService:
  _instance = None

  def __new__(cls, *args, **kwargs):
    
    if cls._instance is None:
      print("Este mensaje solo debe aprecer una vez")
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
    if not hasattr(self, "session_factory"):
      self.session_factory = session_factory

  # def __init__(self, session: AsyncSession):
  #   self.session = session

  async def register(self, data: RegisterInput) -> User:
    async with self.session_factory() as session:
      hash_pw = User.hash_password(data.password)
      new_user = User(
        name=data.name,
        fullname=data.fullname,
        password=hash_pw,
        rol=data.rol,
        email=data.email
      )

      try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
      except Exception as e:
        await session.rollback()
        raise e

      return new_user
  
  async def authenticate(self, data: LoginInput) -> Tuple[User,str,str]:
    async with self.session_factory() as session:
      query = select(User).where(User.email == data.email)
      result = await session.execute(query)
      user: User = result.scalar_one_or_none()

      if not user or not user.verify_password(data.password):
        raise Exception("INVALID CREDENTIALS")
      
      #the user payload
      user_data= {
        "email": user.email,
        "name": user.name,
        "rol": user.rol,
        "id": user.id
      }

      access_token = create_access_token(
        user_data= user_data
      )

      refresh_token = create_access_token(
        user_data=user_data,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
        refresh=True
      )

      return user, access_token, refresh_token
    
  async def get_all_info_by_id(self, id: int) -> User:
    async with self.session_factory() as session:
      query = select(User).where(User.id == id)
      result = await session.execute(query)
      user: User = result.scalar_one_or_none()

      if not user:
        raise Exception("USER NOT FOUND") 
      
      return user