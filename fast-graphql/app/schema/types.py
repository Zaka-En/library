from typing import Optional, List
import strawberry
from datetime import datetime
from strawberry.types import Info
from base64 import b64encode, b64decode
from typing import TypeVar
from broadcaster import Broadcast

broadcast = Broadcast("memory://")

@strawberry.type
class AuthorType(strawberry.relay.Node):
  id: strawberry.relay.NodeID[int]
  name: str
  biography: Optional[str]
  country: str
  fullname: Optional[str]

  @strawberry.field
  def books(self, info: Info) -> List["BookType"]:
    from app.models.book import Book
    from .convertors import book_to_type
    
    session = info.context['db']
    books = session.query(Book).filter(Book.author_id == self.id).all()
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
  def author(self, info: Info) -> Optional["AuthorType"]:
    from app.models.author import Author
    from .convertors import author_to_type
    
    session = info.context['db']
    author = session.query(Author).filter(Author.id == self.author_id).first()
    return author_to_type(author) if author else None

@strawberry.type
class ReadingStateType:
  id: int
  current_page: int 
  start_date: datetime
  finish_date: Optional[datetime]
  book_id: int

  @strawberry.field
  def book(self, info: Info) -> Optional[BookType]:
    from app.models.book import Book
    from .convertors import book_to_type
    
    session = info.context['db']
    book = session.query(Book).filter(Book.id == self.book_id).first()
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

