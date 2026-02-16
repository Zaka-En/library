from .inputs import ( CreateAuthorInput, UpdateAuthorInput, CreateBookInput, UpdateBookInput, StartReadingInput, UpdateProgressInput, FinishReadingInput, RegisterInput, LoginInput )
from .types import AuthorType, BookType, ReadingStateType, UserType, LoginResponse, broadcast
import strawberry
from strawberry.types import Info
from app.models.author import Author
from app.models.book import Book
from app.models.user import User
from app.models.reading_state import ReadingState
from .convertors import *
from datetime import datetime,timedelta
from time import sleep
from fastapi.concurrency import run_in_threadpool
import asyncio
from sqlalchemy import select
from app.utils.auth import create_access_token
from app.utils.permissions import IsAuthenticated
from app.utils.auth import decode_token
from fastapi import Request, Response
from app.services.user_service import UserService
from app.services.author_service import AuthorService
from app.services.book_service import BookService


REFRESH_TOKEN_EXPIRY= 6 * 30


@strawberry.type
class Mutation:
  @strawberry.mutation
  async def register_user(self, info: Info, data: RegisterInput) -> UserType:
    user_service: UserService = info.context["user_service"]

    try:
      new_user = await user_service.register(data=data)
    except Exception as e:
      raise e
    
    return UserType(
      id=strawberry.ID(str(new_user.id)),
      fullname=new_user.fullname,
      name=new_user.name,
      email=new_user.email,
      rol=new_user.rol
    )
      
  @strawberry.mutation
  async def login(self, info: Info, data: LoginInput) -> LoginResponse:
    user_service: UserService = info.context["user_service"]

    user, access_token, refresh_token = await user_service.authenticate(data=data)

    return LoginResponse(
      access_token=access_token,
      refresh_token=refresh_token,
      token_type="bearer",
      user=UserType(
        id=strawberry.ID(str(user.id)),
        email=user.email,
        name=user.name,
        fullname=user.fullname,
        rol=user.rol
      )
    )

  @strawberry.mutation
  async def refresh_token(self, info: Info) -> LoginResponse:

    request: Request = info.context["request"]
    response: Response = info.context["response"]

    refresh_token = request.cookies.get("refresh_token", "")
   
    token_data = decode_token(refresh_token)

    if not token_data.get("refresh"):
        raise Exception("PROVIDED TOKEN IS NOT A REFRESH TOKEN")
    
    exp = token_data.get("exp")
    if not exp or datetime.fromtimestamp(exp) < datetime.now():
        raise Exception("REFRESH TOKEN EXPIRED")
    
    user_data = token_data.get("user")
    if not user_data:
        raise Exception("INVALID TOKEN")
    
    new_access_token = create_access_token(user_data=user_data)

    response.set_cookie(
      key="access_token",
      value=new_access_token,
      httponly=True,
      samesite="strict",
      #secure=True, 
      max_age=900  # 15 minutos
    )

    return LoginResponse(
      access_token=new_access_token,
      refresh_token=refresh_token,
      token_type="bearer"
    )

    """ token_data = decode_token(refresh_token)

    if not token_data.get("refresh"):
      raise Exception("El token proporcionado no es un refresh token")
    
    # verify expiry
    exp = token_data.get("exp")
    if not exp or datetime.fromtimestamp(exp) < datetime.now():
      raise Exception("Refresh token expirado")
    
    # get user data
    user_data = token_data.get("user")
    if not user_data:
      raise Exception("Token inválido")
    
    new_access_token = create_access_token(user_data=user_data)
    
    return LoginResponse(
      access_token=new_access_token,
      refresh_token=refresh_token,
      token_type="bearer"
    )
  """

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def create_author(self, input: CreateAuthorInput, info: Info) -> AuthorType:
    author_service: AuthorService = info.context["author_service"]
    author = await author_service.create(data=input)
    return author_to_type(author=author)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def update_author(self, input: UpdateAuthorInput, info: Info) -> AuthorType:
    author_service: AuthorService = info.context["author_service"]
    author = await author_service.update(data_input=input)
    return author_to_type(author=author)
    

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def delete_author(self, id: int, info: Info) -> bool:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(Author).filter(Author.id == id))
      author = result.scalar_one_or_none()
      if not author:
        return False
      
      await session.delete(author)
      await session.commit()
      return True

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def create_book(self, input: CreateBookInput, info: Info) -> BookType:
    book_service: BookService = info.context["book_service"]
    book = await book_service.create(input=input)
    return book_to_type(book)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def update_book(self, input: UpdateBookInput, info: Info) -> BookType:
    book_service: BookService = info.context["book_service"]
    book = await book_service.update(input=input)
    return book_to_type(book)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def delete_book(self, id: int, info: Info) -> bool:
    return await info.context["book_service"].delete(id=id) 

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def start_reading(self, input: StartReadingInput, info: Info) -> ReadingStateType:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(Book).filter(Book.id == input.book_id))
      book = result.scalar_one_or_none()
      if not book:
        raise ValueError(f"Book with id {input.book_id} not found")
      
      reading_state = ReadingState(
        book_id=input.book_id,
        user_id=input.user_id,
        current_page=1
      )
      
      session.add(reading_state)
      await session.commit()
      await session.refresh(reading_state)
      
      return reading_state_to_type(reading_state)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def update_progress(self, input: UpdateProgressInput, info: Info) -> ReadingStateType:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(ReadingState).filter(ReadingState.id == input.id))
      reading_state = result.scalar_one_or_none()
      if not reading_state:
        raise ValueError(f"ReadingState with id {input.id} not found")
      
      if input.current_page < 0:
        raise ValueError("current_page cannot be negative")
      
      result_book = await session.execute(select(Book).filter(Book.id == reading_state.book_id))
      book = result_book.scalar_one_or_none()
      if book and input.current_page > book.pages:
        raise ValueError(f"current_page ({input.current_page}) cannot exceed total pages ({book.pages})")
      
      reading_state.current_page = input.current_page
      
      await session.commit()
      await session.refresh(reading_state)
      
      return reading_state_to_type(reading_state)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def finish_reading(self, input: FinishReadingInput, info: Info) -> ReadingStateType:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(ReadingState).filter(ReadingState.id == input.id))
      reading_state = result.scalar_one_or_none()
      if not reading_state:
        raise ValueError(f"ReadingState with id {input.id} not found")
      
      reading_state.finish_date = datetime.now()
      
      await session.commit()
      await session.refresh(reading_state)
      
      return reading_state_to_type(reading_state)
  
  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def add_rating(self, text: str) -> str:
    await broadcast.publish(channel="RATINGS",message=text)
    return text

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def generate_reporting(self, author_id: int) -> str:

    def heavy_work():
      print("heavy work")
      sleep(10)
      return "report generated"
    

    result = await run_in_threadpool(heavy_work)
    return f"hecho {result}"
  
  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def send_book_chat_message(
    self,
    book_id: int,
    user_name: str,
    message: str
  ) -> bool:
    
    channel = f"BOOK_CHAT_{book_id}"

    payload = f"{user_name}: {message}"

    await broadcast.publish(channel=channel, message=payload)

    return True