from fastapi import Depends, HTTPException
from typing import Annotated, Any
from app.database import get_db_session
from app.broadcast import broadcast
from app.services.user_service import UserService
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.reading_state_service import ReadingStateService
from app.schema.loaders import create_loaders
from app.utils.auth import decode_token

async def get_user_service(session=Depends(get_db_session)):
  return UserService(session=session)

async def get_author_service(session=Depends(get_db_session)):
  return AuthorService(session=session, broadcast=broadcast)

async def get_book_service(session=Depends(get_db_session)):
  return BookService(session=session)

async def get_reading_state_service(session=Depends(get_db_session)):
  return ReadingStateService(session=session)


async def get_context(
    user_service: Annotated[UserService,Depends(get_user_service)],
    author_service: Annotated[AuthorService,Depends(get_author_service)],
    book_service: Annotated[BookService,Depends(get_book_service)],
    reading_state_service: Annotated[ReadingStateService,Depends(get_reading_state_service)],
  )-> dict[str, Any]:
  
  print("="*89)
  return {
    #"request": request, Injected by strawberry
    #"response": response,
    "user_service": user_service,
    "author_service": author_service,
    "book_service": book_service,
    "reading_state_service": reading_state_service,
    **create_loaders(book_service=book_service,author_service=author_service)
  }


async def parse_jwt_data(token: str) -> dict[str, str]:
  try:
    payload = decode_token(token=token)
  except:
    raise HTTPException(status_code=401,detail="INVALID CREDENTIALS")
  
  user= payload["user"]
  return {"user": user}
  
