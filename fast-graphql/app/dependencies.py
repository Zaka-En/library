from fastapi import Depends,  Request, WebSocket
from typing import Annotated, Any, Union
from app.database import  SessionLocal
from app.broadcast import broadcast
from app.services.user_service import UserService
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.reading_state_service import ReadingStateService
from app.schema.loaders import create_loaders
from app.utils.auth import decode_token
#from strawberry.fastapi import  BaseContext
from jwt import exceptions as pyJwtExceptions

async def get_user_service():
  return UserService(session_factory=SessionLocal)

async def get_author_service():
  return AuthorService(session_factory=SessionLocal, broadcast=broadcast)

async def get_book_service():
  return BookService(session_factory=SessionLocal)

async def get_reading_state_service():
  return ReadingStateService(session_factory=SessionLocal)


def parse_jwt_data_to_user(request: Request | WebSocket) -> dict | None:
  access_token = ""
  
  if isinstance(request, Request):
    access_token = request.cookies.get("access_token", "") if request.cookies is not None else None
  if not access_token:
    print("En este contexto no hay nigun usuario")
    return None

  try:
    payload = decode_token(access_token)
    user = payload.get("user")
    
    return user
  except pyJwtExceptions.InvalidTokenError as e:
    print(f"Error decodificando el token: {e}")
    return None
  except Exception as e:
    print(f"Error decodificando el token: {e}")
    return None

# def require_roles(user: Depends(parse_jwt_data_to_user)):

#TODO convert the get_context to return a CustomContext instance extending from strawberry.BaseContext
async def get_context(
    request: Request,
    user_service: Annotated[UserService,Depends(get_user_service)],
    author_service: Annotated[AuthorService,Depends(get_author_service)],
    book_service: Annotated[BookService,Depends(get_book_service)],
    reading_state_service: Annotated[ReadingStateService,Depends(get_reading_state_service)],
  )-> dict[str, Any]:

  print("Nos ha llegado un objeto Websocket si o no", isinstance(request,WebSocket))
  
  return {
    #"request": request,
    #"response": response,
    "user_service": user_service,
    "author_service": author_service,
    "book_service": book_service,
    "reading_state_service": reading_state_service,
    "user": parse_jwt_data_to_user(request) if request else None,
    "user_access_token": request.cookies.get("access_token", "") if request and request.cookies else None,
    **create_loaders(book_service=book_service,author_service=author_service)
  }


