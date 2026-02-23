from typing import Optional, List, Any
import strawberry
from datetime import datetime
from strawberry.types import Info
from typing import TypeVar
from strawberry.dataloader import DataLoader
from app.dependencies import CustomContext
from app.models.user import User
from app.utils.permissions import RBAC


@strawberry.type
class AuthorType(strawberry.relay.Node):
  id: strawberry.relay.NodeID[int]
  name: str
  biography: Optional[str]
  country: str
  fullname: Optional[str]

  @strawberry.field
  async def books(self, info: Info[CustomContext,Any]) -> List["BookType"]:
    from .convertors import book_to_type
    books = await info.context.loaders.book.load(self.id)
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
  async def author(self, info: Info[CustomContext,Any]) -> Optional["AuthorType"]:
    from .convertors import author_to_type
    auhtor_loader: DataLoader = info.context.loaders.author
    author = await auhtor_loader.load(self.id)
    return author_to_type(author)
  
@strawberry.type
class ReadingStateType:
  id: int
  current_page: int 
  start_date: datetime
  finish_date: Optional[datetime]
  book_id: int

  @strawberry.field
  async def book(self, info: Info[CustomContext,Any]) -> Optional[BookType]:
    from .convertors import book_to_type
    book = await info.context.loaders.book.load(self.book_id)
    return book_to_type(book) if book else None
  
@strawberry.type
class UserType:
  id: strawberry.ID
  email: str
  name: str
  fullname: Optional[str]
  rol: str

@strawberry.type
class UserProfileType(User):
  id: strawberry.ID
  email: Optional[str]
  name: Optional[str]
  username: Optional[str]
  fullname: Optional[str]
  rol: Optional[str]= strawberry.field(permission_classes=[RBAC("admin")])
  second_name: Optional[str] 
  street_adress: Optional[str]
  city: Optional[str]
  province: Optional[str]
  zip_code: Optional[str]
  about: Optional[str]

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


