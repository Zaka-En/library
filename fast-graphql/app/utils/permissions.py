from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any
from fastapi import Request, Response, status
from app.utils.auth import decode_token
from functools import lru_cache
from jwt import exceptions as pyJwtExceptions

class IsAuthenticated(BasePermission):
  message = "UNAUTHENTICATED"

  def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
    request: Request = info.context.get("request")
    response: Response = info.context.get("response")
    
    access_token: str = request.cookies.get("access_token", "")

    if not access_token:
      response.status_code = status.HTTP_401_UNAUTHORIZED
      return False

    try:
      decoded = decode_token(access_token)
      if decoded.get("refresh"):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return False

    except pyJwtExceptions.ExpiredSignatureError :
      self.message = "UNAUTHENTICATED, TOKEN EXPIRED"
      response.status_code = status.HTTP_401_UNAUTHORIZED
      return False
    except pyJwtExceptions.InvalidTokenError :
      self.message = "UNAUTHENTICATED, INVALID TOKEN"
      response.status_code = status.HTTP_401_UNAUTHORIZED
      return False
    except Exception as e:
      self.message = "ERROR DECODING TOKEN"
      response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
      return False
    
    return True
  
  
    
@lru_cache
def RBAC(*roles: str):
  class RoleBasedAccessControl(BasePermission):
    message = f"UNAUTHORIZED. REQUIRED ROLES: {', '.join(roles)}"

    def has_permission(self, source: Any, info: Info[Any, Any], **kwargs: Any) -> bool:

      auth_cheking = IsAuthenticated()
      if not auth_cheking.has_permission(source=source,info=info,**kwargs):
        return False
      
      response: Response = info.context["response"]
      
      user_access_token = info.context["user_access_token"]


      # try:
      #   payload = decode_token(user_access_token)
      #   user = payload.get("user")
        
      #   return user
      # except pyJwtExceptions.InvalidTokenError as e:
      #   print(f"Error decodificando el token: {e}")
      #   return None
      # except Exception as e:
      #   print(f"Error decodificando el token: {e}")
      #   return None

      # if not user:
      #   response.status_code = status.HTTP_500
      #   return False

      # if user.get("rol") not in roles:
      #   response.status_code = status.HTTP_403_FORBIDDEN
      #   return False
      
      return True

  return RoleBasedAccessControl
      
      


#TODO: METER EN DEPENDENCIES
# usedPemissions = set()

# @cached
# def RBAC(roles):
#   ....
