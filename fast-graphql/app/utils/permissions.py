from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any

class IsAuthenticated(BasePermission):
  message = "User not authenticated or invalid token"

  def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
    user = info.context.get("user")
    return user is not None