from typing import Optional, List
import strawberry
from datetime import datetime
from strawberry.types import Info
from base64 import b64encode, b64decode
from typing import Generic, TypeVar

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



def encode_user_cursor(id: int) -> str:
    """
    Encodes the given user ID into a cursor.

    :param id: The user ID to encode.

    :return: The encoded cursor.
    """
    return b64encode(f"user:{id}".encode("ascii")).decode("ascii")


def decode_user_cursor(cursor: str) -> int:
    """
    Decodes the user ID from the given cursor.

    :param cursor: The cursor to decode.

    :return: The decoded user ID.
    """
    cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
    return int(cursor_data.split(":")[1])


GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
  page_info: "PageInfo" = strawberry.field(
      description="Information to aid in pagination."
  )

  edges: list["Edge[GenericType]"] = strawberry.field(
      description="A list of edges in this connection."
  )


@strawberry.type
class PageInfo:
  has_next_page: bool = strawberry.field(
      description="When paginating forwards, are there more items?"
  )

  has_previous_page: bool = strawberry.field(
      description="When paginating backwards, are there more items?"
  )

  start_cursor: Optional[str] = strawberry.field(
      description="When paginating backwards, the cursor to continue."
  )

  end_cursor: Optional[str] = strawberry.field(
      description="When paginating forwards, the cursor to continue."
  )


@strawberry.type
class Edge(Generic[GenericType]):
  node: GenericType = strawberry.field(description="The item at the end of the edge.")

  cursor: str = strawberry.field(description="A cursor for use in pagination.")

