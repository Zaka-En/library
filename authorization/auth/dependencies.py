from .service import decode_token
from fastapi import HTTPException
from .database import SessionLocal

def validate_token_signature(token: str):
  try:
    decode_token(token)
    
  except Exception :
    raise HTTPException(status_code=401 ,detail="INVALID_TOKEN")
  print("DEBUG: HEMOS VALIDADO EL TOKEN")
  return token

  
async def get_db_session():
  async with SessionLocal() as session:
    yield session
  