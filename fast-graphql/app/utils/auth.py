import jwt
import uuid
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os
from typing import Optional, Any

load_dotenv()

SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRY = 60 #15 * 60



def create_access_token(
  user_data: dict,
  expiry: Optional[timedelta] = None,
  refresh: bool = False
  ):
  
  payload: dict[str, Any] = {}

  payload["user"] = user_data
  payload["exp"] = datetime.now(timezone.utc) + (
    expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
  )
  payload["jti"] = str(uuid.uuid4())

  payload["refresh"] = refresh

  token = jwt.encode(
    payload=payload,
    key=SECRET_KEY,
    algorithm=ALGORITHM
  )

  return token


def decode_token(token: str) -> dict[str,Any] :
  try:
    token_data = jwt.decode(
      jwt=token,
      key=SECRET_KEY,
      algorithms=[ALGORITHM]
    )
    
    return token_data
  except jwt.PyJWTError as e:
    raise e
