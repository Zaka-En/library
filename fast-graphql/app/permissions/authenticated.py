from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any
from fastapi import  Response
from app.dependencies import CustomContext

class IsAuthenticated(BasePermission):
  message = "UNAUTHENTICATED"

  def has_permission(self, source: Any, info: Info[CustomContext, Any], **kwargs) -> bool:
    
    auth = info.context.auth
    response: Response | None = info.context.response

    if not auth.is_authenticated:
      self.message = auth.error_message
      if response:
        response.status_code = auth.status_code
      return False

    return True   