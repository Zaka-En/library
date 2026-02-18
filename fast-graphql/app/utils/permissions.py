from collections.abc import Awaitable
from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any, Awaitable
from fastapi import Request, Response, status
from app.utils.auth import decode_token

class IsAuthenticated(BasePermission):
  message = "UNAUTHENTICATED"

  def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
    request: Request = info.context.get("request")
    response: Response = info.context.get("response")

    if not request and response:
      response.status_code = status.HTTP_401_UNAUTHORIZED
      return False
    
    access_token: str = request.cookies.get("access_token", "")

    if not access_token:
      response.status_code = status.HTTP_401_UNAUTHORIZED
      return False

    try:

      decoded = decode_token(access_token)

      if not decoded or decoded.get("refresh"):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return False

      info.context["user"] = decoded["user"]

      return True
    
    except Exception as e :
      return False

def RBAC(*roles):
  class RBAC(BasePermission):
    message = f"UNAUTHORIZED. REQUIRED ROLES: {', '.join(roles)}"

    def has_permission(self, source: Any, info: Info[Any, Any], **kwargs: Any) -> bool | Awaitable[bool]:

      auth_cheking = IsAuthenticated()
      if not auth_cheking.has_permission(source=source,info=info,**kwargs):
        return False
      
      


#TODO: METER EN DEPENDENCIES
# usedPemissions = set()

# @cached
# def RBAC(roles):
#   ....
