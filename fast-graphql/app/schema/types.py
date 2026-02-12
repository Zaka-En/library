from typing import Optional, List
import strawberry
from datetime import datetime
from strawberry.types import Info
from sqlalchemy import select
from typing import TypeVar
from broadcaster import Broadcast
from app.models.author import Author
from app.models.book import Book

broadcast = Broadcast("redis://localhost:6379")

@strawberry.type
class AuthorType(strawberry.relay.Node):
  id: strawberry.relay.NodeID[int]
  name: str
  biography: Optional[str]
  country: str
  fullname: Optional[str]

  @strawberry.field
  async def books(self, info: Info) -> List["BookType"]:
    from .convertors import book_to_type
    async with info.context['db_factory']() as session:
      query = select(Book).filter(Book.author_id == self.id)
      result = await session.execute(query)
      books = result.scalars().all()
      return [book_to_type(book) for book in books]

@strawberry.type
class BookType:
  id: int
  title: str 
  isbn: str
  publication_year: int
  pages: int
  author_id: int

  @strawberry.field
  async def author(self, info: Info) -> Optional["AuthorType"]:
    from .convertors import author_to_type
    async with info.context['db_factory']() as session:
      result = await session.execute(
        select(Author).filter(Author.id == self.author_id)
      )
      author = result.scalar_one_or_none()
      return author_to_type(author) if author else None

@strawberry.type
class ReadingStateType:
  id: int
  current_page: int 
  start_date: datetime
  finish_date: Optional[datetime]
  book_id: int

  @strawberry.field
  async def book(self, info: Info) -> Optional[BookType]:
    from .convertors import book_to_type
    async with info.context['db_factory']() as session:
      result = await session.execute(
        select(Book).filter(Book.id == self.book_id)
      )
      book = result.scalar_one_or_none()
      return book_to_type(book) if book else None

@strawberry.type
class CustomPageInfo(strawberry.relay.PageInfo):
  """PageInfo extended with aditional info"""
  total_count: int

NodeType = TypeVar("NodeType")

@strawberry.type
class AuthorConnection:
  page_info: CustomPageInfo
  edges: list[strawberry.relay.Edge[AuthorType]]