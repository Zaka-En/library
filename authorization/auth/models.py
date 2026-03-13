from pydantic import BaseModel, EmailStr
from typing import Literal

class UserPayload(BaseModel):
  id: int
  email: EmailStr
  name: str
  rol: Literal['admin', 'user', 'editor']


class AuthResponse(BaseModel):
  access_token: str | None = None
  message: Literal[
    "AUTHENTICATED",
    "TOKEN_REFRESHED",
  ]


class TokenRequest(BaseModel):
  grant_type: Literal["authorization_code", "refresh_token"]
  token: str 


class TokensResponse(BaseModel):
  access_token: str 
  refresh_token: str


class RevokeTokenResponse(BaseModel):
  success: bool