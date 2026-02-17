from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any
from fastapi import Request
from app.utils.auth import decode_token

#TODO devolver 40* en vez de mensaje
class IsAuthenticated(BasePermission):
  message = "Token expired"

  def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
    request: Request = info.context.get("request")

    if not request:
      return False
    
    access_token: str = request.cookies.get("access_token", "")

    try:

      decoded = decode_token(access_token)

      if decoded.get("refresh"):
        return False
      
      info.context["user"] = decoded["user"]

      return True
    
    except Exception as e :
      return False

#TODO: METER EN DEPENDENCIES
usedPemissions = set()

@cached
def RBAC(roles):
  ....
