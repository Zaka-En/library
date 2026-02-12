from .inputs import ( CreateAuthorInput, UpdateAuthorInput, CreateBookInput, UpdateBookInput, StartReadingInput, UpdateProgressInput, FinishReadingInput )
from .types import AuthorType, BookType, ReadingStateType, broadcast
import strawberry
from strawberry.types import Info
from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .convertors import *
from datetime import datetime
from time import sleep
from random import randint
from fastapi.concurrency import run_in_threadpool
import asyncio
from sqlalchemy import select


@strawberry.type
class Mutation:

  @strawberry.mutation
  async def create_author(self, input: CreateAuthorInput, info: Info) -> AuthorType:
    async with info.context['db_factory']() as session:
      author = Author(
        name=input.name,
        biography=input.biography,
        fullname=input.fullname,
        country=input.country
      )

      session.add(author)
      await session.commit()
      await session.refresh(author)

      return author_to_type(author)

  @strawberry.mutation
  async def update_author(self, input: UpdateAuthorInput, info: Info) -> AuthorType:

    await broadcast.publish(channel="NOTIFICATIONS", message="Incializando actualizacion")
    await asyncio.sleep(3)
    await broadcast.publish(channel="NOTIFICATIONS", message="Validando sus datos")
    await asyncio.sleep(3)

    async with info.context['db_factory']() as session:
      result = await session.execute(select(Author).filter(Author.id == input.id))
      author = result.scalar_one_or_none()
      if not author:
        raise ValueError(f"Author with id {input.id} not found")
      
      
      input_dict = vars(input)
      
      for key, value in input_dict.items():
        if key != 'id' and value is not None:
          setattr(author, key, value)

      try:
        await session.commit()
        await session.refresh(author)
      except Exception as e:
        await session.rollback()
        raise e
      
      await broadcast.publish(channel="NOTIFICATIONS", message="¡Autor actualizado con éxito!")
      await asyncio.sleep(3)

      return author_to_type(author)

  @strawberry.mutation
  async def delete_author(self, id: int, info: Info) -> bool:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(Author).filter(Author.id == id))
      author = result.scalar_one_or_none()
      if not author:
        return False
      
      await session.delete(author)
      await session.commit()
      return True

  @strawberry.mutation
  async def create_book(self, input: CreateBookInput, info: Info) -> BookType:
    await asyncio.sleep(1)
    async with info.context['db_factory']() as session:
      result = await session.execute(select(Book).filter(Book.isbn == input.isbn))
      isbnAlreadyExists = result.scalar_one_or_none()

      if isbnAlreadyExists:
        raise Exception("UNIQUE ISBN RULE VIOLATED")   
      elif len(input.isbn) < 13:
        raise  Exception("INVALID ISBN: exactly 13 characters")   

      book = Book(
        title=input.title,
        isbn=input.isbn,
        publication_year=input.publication_year,
        pages=input.pages,
        author_id=input.author_id
      )
      
      session.add(book)
      await session.commit()
      await session.refresh(book)
      
      return book_to_type(book)

  @strawberry.mutation
  async def update_book(self, input: UpdateBookInput, info: Info) -> BookType:
    await asyncio.sleep(2)

    if randint(1, 2) == 2:
      raise Exception("ha fallado porque no tiene suerte")

    async with info.context['db_factory']() as session:
      result = await session.execute(select(Book).filter(Book.id == input.id))
      book = result.scalar_one_or_none()
      if not book:
        raise ValueError(f"Book with id {input.id} not found")
      
     
      input_dict = vars(input)

      for key, value in input_dict.items():
        if key != 'id' and value is not None:
          setattr(book,key,value)
      
      await session.commit()
      await session.refresh(book)
      
      return book_to_type(book)

  @strawberry.mutation
  async def delete_book(self, id: int, info: Info) -> bool:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(Book).filter(Book.id == id))
      book = result.scalar_one_or_none()
      if not book:
        return False
      
      await session.delete(book)
      await session.commit()
      return True

  @strawberry.mutation
  async def start_reading(self, input: StartReadingInput, info: Info) -> ReadingStateType:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(Book).filter(Book.id == input.book_id))
      book = result.scalar_one_or_none()
      if not book:
        raise ValueError(f"Book with id {input.book_id} not found")
      
      reading_state = ReadingState(
        book_id=input.book_id,
        user_id=input.user_id,
        current_page=0
      )
      
      session.add(reading_state)
      await session.commit()
      await session.refresh(reading_state)
      
      return reading_state_to_type(reading_state)

  @strawberry.mutation
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

  @strawberry.mutation
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
  
  @strawberry.mutation
  async def add_rating(self, text: str) -> str:
    await broadcast.publish(channel="RATINGS",message=text)
    return text

  @strawberry.mutation
  async def generate_reporting(self, author_id: int) -> str:

    def heavy_work():
      print("heavy work")
      sleep(10)
      return "report generated"
    

    result = await run_in_threadpool(heavy_work)
    return f"hecho {result}"
  
  @strawberry.mutation
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