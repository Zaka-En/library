from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any
from fastapi import  Response, HTTPException, status
from app.dependencies import CustomContext
from app.services.auth_service import AuthService

class IsAuthenticated(BasePermission):
  message = "UNAUTHENTICATED, INVALID TOKEN [BACKEND]"
  
  #TODO: refactorizar esta mierda
  async def has_permission(self, source: Any, info: Info[CustomContext, Any], **kwargs) -> bool:
    response: Response | None = info.context.response

    access_token = info.context.access_token
    # refresh_token = info.context.refresh_token
    # retried = False



    try:
      token, auth_message = await AuthService.validate_token(access_token)
      print(f"INFO: TOKEN VALIDADTED {token[:11]}... {auth_message}")
    except HTTPException as e:
      print("=====================================")
      print(f"DEGUB: the auth error produced is: {e.detail}")

      self.message = e.detail

      if response:
        response.status_code = status.HTTP_401_UNAUTHORIZED

      return False
    except Exception as e:
      print(f"DEBUG: Unexpected error: {str(e)}")
      self.message = "AUTH_INTERNAL_ERROR"
      if response:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
      return False
      
    return True

  # async def _refresh_access_token(self, refresh_token: str) -> tuple[str, str] | None:
  #   try:
  #     new_access_token, message = await AuthService.refresh_token(refresh_token)
  #     return new_access_token, message
  #   except Exception as e:
  #     detail = str(e)
  #     print(F"EL FALLO DE REFRESHING {detail}")
  #     if detail == "SERVER_ERROR":
  #       raise  
  #     return None