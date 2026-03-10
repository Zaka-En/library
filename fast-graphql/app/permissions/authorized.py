from .authenticated import IsAuthenticated
from strawberry.types import Info
from typing import Any
from fastapi import  Response, status
from functools import lru_cache
from app.dependencies import CustomContext

    
@lru_cache
def RBAC(*roles: str):
  class RoleBasedAccessControl(IsAuthenticated):
    message = f"UNAUTHORIZED. REQUIRED ROLES: {', '.join(roles)}"

    async def has_permission(self, source: Any, info: Info[CustomContext, Any], **kwargs: Any) -> bool:

      # Before cheking the authorization, vemos si está autenticado
      auth_check = await super().has_permission(source, info, **kwargs)
      print(f"AUTH CHECK : {auth_check}")
      response: Response | None = info.context.response

      if not auth_check:
        if response:
          response.status_code = status.HTTP_401_UNAUTHORIZED
        return False
      
      user = info.context.user
      print(user)

      if user and user["rol"] not in roles:
        print(user["rol"])
        if response:
          response.status_code = status.HTTP_403_FORBIDDEN
          return False
      
      print("somehow the request reaches this place when it shoudnt")
      return True

  return RoleBasedAccessControl