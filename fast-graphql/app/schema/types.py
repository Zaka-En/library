from typing import Optional, List
import strawberry
from datetime import datetime
from strawberry.types import Info
from typing import TypeVar
from broadcaster import Broadcast
from strawberry.dataloader import DataLoader


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
    books = await info.context["books_by_author_loader"].load(self.id)  
    return [book_to_type(b) for b in books] 
  
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
    auhtor_loader: DataLoader = info.context["author_loader"]
    author = await auhtor_loader.load(self.author_id)
    return author_to_type(author)
  
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
    book = await info.context["book_loader"].load(self.book_id)  
    return book_to_type(book) if book else None
  
@strawberry.type
class UserType:
  id: strawberry.ID
  email: str
  name: str
  fullname: Optional[str]
  rol: str

@strawberry.type
class LoginResponse:
  access_token: str
  refresh_token : str
  token_type: str
  user: Optional[UserType] = None

@strawberry.type
class CustomPageInfo(strawberry.relay.PageInfo):
  """PageInfo extended with aditional info"""
  total_count: int

NodeType = TypeVar("NodeType")

@strawberry.type
class AuthorConnection:
  page_info: CustomPageInfo
  edges: list[strawberry.relay.Edge[AuthorType]]