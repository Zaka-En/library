from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schema.inputs import RegisterInput, LoginInput
from app.models.user import User
from app.utils.auth import create_access_token
from datetime import timedelta
from typing import Tuple

REFRESH_TOKEN_EXPIRY=120 #6 months

class UserService:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def register(self, data: RegisterInput) -> User:
    hash_pw = User.hash_password(data.password)
    new_user = User(
      name=data.name,
      fullname=data.fullname,
      password=hash_pw,
      rol=data.rol,
      email=data.email
    )

    try:
      self.session.add(new_user)
      await self.session.commit()
      await self.session.refresh(new_user)
    except Exception as e:
      await self.session.rollback()
      raise e

    return new_user
  
  async def authenticate(self, data: LoginInput) -> Tuple[User,str,str]:
    query = select(User).where(User.email == data.email)
    result = await self.session.execute(query)
    user: User = result.scalar_one_or_none()

    if not user or not user.verify_password(data.password):
      raise Exception("INVALID CREDENTIALS")
    
    user_data= {
      "email": user.email,
      "name": user.name,
      "rol": user.rol
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