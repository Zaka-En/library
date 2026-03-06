from fastapi import APIRouter, HTTPException, status, Depends
from ..service import create_access_token, decode_token, revoke_token as revoke, is_black_listed
from ..models import AuthResponse, TokenRequest, UserPayload, TokensResponse, RevokeTokenResponse
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import timedelta
from typing import Annotated
from ..dependencies import get_jti, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/token", response_model=AuthResponse)
async def validate_or_refresh_token(
  body: TokenRequest,
  db_session: Annotated[AsyncSession, Depends(get_db_session)]
  ):

  token = body.token
  grant_type = body.grant_type

  try:
    decoded = decode_token(token)
    print(f"DEBUG: token has been decoded  {decoded}")
    
    if grant_type == "authorization_code" and decoded.get("refresh", False):
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="ACCESS_WITH_REFRESH_TOKEN_FORBIDDEN"
      )
        
    user = decoded["user"]

    if grant_type == "refresh_token":
      
      jti = decoded["jti"]
      print(f"DEBUG: el jti es:  {jti}")
      is_blacklisted = await is_black_listed(jti, db_session)
      print(f"DEBUG: el blacklisted check se ejecuto y este su resultado {is_black_listed}")
      if is_blacklisted:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="REFRESH_TOKEN_BLACKLISTED"
      )

      new_access_token = create_access_token(user)
      print(f"DEBUG:  se ha emitido un nuevo token {new_access_token}")
      return AuthResponse(message="TOKEN_REFRESHED", access_token=new_access_token)
    
    return AuthResponse(message="AUTHENTICATED", access_token=token)

  except ExpiredSignatureError:
    error_msg = "REFRESH_TOKEN_EXPIRED" if grant_type == "refresh_token" else "ACCESS_TOKEN_EXPIRED"
    print(f"DEBUG:  {error_msg}")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_msg)
  
  except InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_TOKEN")
  
      
  except Exception as e:
    print(f"DEBUG 500: {str(e)}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="AUTH_ERROR")

@router.post("/authorize", response_model=TokensResponse)
async def create_tokens(user_payload: UserPayload):
  user_data = user_payload.model_dump()
  access_token = create_access_token(user_data=user_data)
  refresh_token = create_access_token(
    user_data=user_data, 
    refresh=True, 
    expiry=timedelta(days=90)
  )

  return TokensResponse(
    access_token=access_token,
    refresh_token=refresh_token
  )


@router.post("/revoke", response_model=RevokeTokenResponse)
async def revoke_token(
  token: str,
  db_session: Annotated[AsyncSession, Depends(get_db_session)], 
  ):

  try:
    jti = get_jti(token)
  except HTTPException as e:
    raise e
  
  
  if not jti:
    return False
  
  success = await revoke(jti, db_session)

  return RevokeTokenResponse(success=success)

@router.get("/")
async def hola():
  return {"message":"auth server running"}
  
