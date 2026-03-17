from fastapi import HTTPException

from .database import SessionLocal
from .service import decode_token


def get_jti(token: str) -> str:
    try:
        decoded = decode_token(token)
        jti = decoded["jti"]
    except Exception:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")
    print("DEBUG: HEMOS VALIDADO EL TOKEN")
    return jti


async def get_db_session():
    async with SessionLocal() as session:
        yield session
