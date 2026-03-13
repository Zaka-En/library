from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any
from fastapi import  Response, Request, status
from app.dependencies import CustomContext
from app.services.auth_service import AuthService

class IsAuthenticated(BasePermission):
  message = "UNAUTHENTICATED"
  
  #TODO: refactorizar esta mierda
  async def has_permission(self, source: Any, info: Info[CustomContext, Any], **kwargs) -> bool:
    response: Response | None = info.context.response

    access_token = info.context.access_token
    refresh_token = info.context.refresh_token
    retried = False

    try:
      token, auth_message = await AuthService.validate_token(access_token)
      print(f"INFO: TOKEN VALIDADTED {token[:11]}... {auth_message}")
    except Exception as e:
      detail = str(e)

      if detail == "ACCESS_TOKEN_EXPIRED" and not retried:
        print(f"TOKEN EXPIRED: REFRESHINg")
        retried = True
        refreshed = await self._refresh_access_token(refresh_token)
        if refreshed:
          new_access_token, auth_message = refreshed
          print(f"TOKEN EMITTED: {auth_message}: {new_access_token[:11]}")
          info.context.access_token = new_access_token
          return True
        else:
          if response:
            response.status_code = status.HTTP_401_UNAUTHORIZED
          return False
      elif detail == "SERVER_ERROR" and response:
        self.message = detail
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return False
      else:
        if response:
          response.status_code = status.HTTP_401_UNAUTHORIZED
        return False
      
    return True

  async def _refresh_access_token(self, refresh_token: str) -> tuple[str, str] | None:
    try:
      new_access_token, message = await AuthService.refresh_token(refresh_token)
      return new_access_token, message
    except Exception as e:
      detail = str(e)
      print(F"EL FALLO DE REFRESHING {detail}")
      if detail == "SERVER_ERROR":
        raise  
      return None
  