from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from app.models.book import Book
from app.models.author import Author
from typing import Optional, List
from app.schema.inputs import CreateBookInput, UpdateBookInput
from .base import BaseService, SingletonServiceInstance


class BookService(SingletonServiceInstance,BaseService[Book]):

  def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
    if not hasattr(self, "session_factory"):
      self.session_factory = session_factory

  async def get_all(self) -> List[Book]:
    async with self.session_factory() as session:
      result = await session.execute(select(Book))
      return list(result.scalars().all())

  async def get_by_id(self, book_id: int) -> Book:
    async with self.session_factory() as session:
      result = await session.execute(select(Book).filter(Book.id == book_id))
      return result.scalar_one_or_none()

  async def get_by_ids(self, books_ids: list[int]) -> List[Book]:
    async with self.session_factory() as session:
      return list((await session.execute(select(Book).where(Author.id.in_(books_ids)))).scalars().all())

  async def get_by_author_ids(self, authors_ids: list[int]) -> List[Book]:
    async with self.session_factory() as session:
      return list((await session.execute(select(Book).where(Book.author_id.in_(authors_ids)))).scalars().all())

  async def create(self, data: CreateBookInput):
    async with self.session_factory() as session:
      author_check = await session.execute(select(Author).filter(Author.id == data.author_id))
      if not author_check.scalar_one_or_none():
        raise ValueError(f"No se puede crear el libro: El autor {data.author_id} no existe")
      IsbnQuery = await session.execute(select(Book).filter(Book.isbn == data.isbn))
      isbnAlreadyExists = IsbnQuery.scalar_one_or_none()
      if isbnAlreadyExists:
        raise Exception("UNIQUE ISBN RULE VIOLATED")
      elif len(data.isbn) < 13:
        raise Exception("INVALID ISBN: exactly 13 characters")
      new_book: Book = Book(
        title=data.title,
        isbn=data.isbn,
        author_id=data.author_id,
        publication_year=data.publication_year,
        pages=data.pages
      )
      session.add(new_book)
      await session.commit()
      await session.refresh(new_book)
      return new_book

  async def update(self, data: UpdateBookInput) -> Optional[Book]:
    async with self.session_factory() as session:
      result = await session.execute(select(Book).filter(Book.id == data.id))
      book = result.scalar_one_or_none()
      if not book:
        return None
      data_dict = vars(data)
      for key, value in data_dict.items():
        if key != 'id' and value is not None:
          setattr(book, key, value)
      await session.commit()
      await session.refresh(book)
      return book

  async def delete(self, id: int) -> bool:
    async with self.session_factory() as session:
      result = await session.execute(select(Book).filter(Book.id == id))
      book = result.scalar_one_or_none()
      if not book:
        return False
      await session.delete(book)
      await session.commit()
      return True

  async def get_by_author(self, author_id: int) -> List[Book]:
    async with self.session_factory() as session:
      query = select(Book).filter(Book.author_id == author_id)
      result = await session.execute(query)
      return list(result.scalars().all())