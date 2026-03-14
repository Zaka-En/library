from app.config import settings
from aiohttp import ClientSession
from app.models.user import UserPayload
from typing import Tuple
from fastapi import HTTPException

AUTHORIZE_ENDPOINT = settings.auth_service_url + "/oauth/authorize"
REFRESH_VALIDTE_ENDPOINT = settings.auth_service_url + "/oauth/token"
REVOKE_TOKEN_ENDPOINT = settings.auth_service_url + "/oauth/revoke"

class AuthService:

  @staticmethod
  async def get_tokens(user_payload:  UserPayload) -> Tuple[str,str]:
    async with ClientSession() as session:
      async with session.post(
        AUTHORIZE_ENDPOINT,
        json=user_payload.model_dump()
        ) as response:

        if response.status != 200:
          raise HTTPException(
            status_code=response.status,
            detail="AUTH_SERVICE_ERROR"
          )

        data = await response.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        return (access_token, refresh_token)
      
  @staticmethod
  async def validate_token(token: str) -> Tuple[str, str]:
    async with ClientSession() as session:
      grant_type = "authorization_code"
      body = {
        "grant_type" : grant_type,
        "token": token
      }

      async with session.post(
        REFRESH_VALIDTE_ENDPOINT,
        json=body
        ) as response:

      
        data = await response.json()
        response_status_code = response.status
        
        if response_status_code != 200:
          raise HTTPException(
            status_code=response_status_code,
            detail=data["detail"])

        
        token = data["access_token"]
        message =  data["message"]

        return (token, message)

  @staticmethod
  async def refresh_token(token: str) -> Tuple[str, str]:
    async with ClientSession() as session:
      grant_type = "refresh_token"
      body = {
        "grant_type" : grant_type,
        "token": token
      }

      async with session.post(
        REFRESH_VALIDTE_ENDPOINT,
        json=body
        ) as response:

        data = await response.json()
        response_status_code = response.status


        if response_status_code != 200:
          raise HTTPException(
            status_code=response_status_code,
            detail=data["detail"]
          )

        token = data["access_token"]
        message =  data["message"]
        
        return (token, message)

  @staticmethod     
  async def revoke_token(token: str) -> bool:
    async with ClientSession() as session:
      async with session.post(
        REVOKE_TOKEN_ENDPOINT,
        params={"token":token},
        
      ) as response :
        
        data: dict = await response.json()

        success: bool = data.get("success", False)

        return success 
