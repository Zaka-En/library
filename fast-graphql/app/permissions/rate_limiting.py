
from strawberry.permission import BasePermission
from strawberry.types import Info
from typing import Any
from fastapi import  Response, status
from functools import lru_cache
from app.dependencies import CustomContext
from app.limiter import limiter, RateLimitExceeded

@lru_cache
def rate_limiting(limit:int, seconds:int):
  class RateLimit(BasePermission):
    message = "TOO MANY REQUESTS"

    def has_permission(self, source: Any, info: Info[CustomContext, Any], **kwargs):
      request = info.context.request

      try:
        @limiter.limit(f"{limit}/{seconds}")
        def check_limit(request):
          pass
        
        check_limit(request)
        return True
      except RateLimitExceeded:
        response: Response | None = info.context.response
        if response:
          response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        return False
      except Exception as e:
        response: Response | None = info.context.response
        if response:
          response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = F"RATE LIMIT RESOLVE FAILED {e}"
        return False
  return RateLimit