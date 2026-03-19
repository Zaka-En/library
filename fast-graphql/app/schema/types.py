from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, TypeVar

import strawberry
from strawberry.dataloader import DataLoader
from strawberry.types import Info

from app.models.user import User
from app.permissions.authorized import RBAC

# if TYPE_CHECKING:
#     from app.dependencies import CustomContext


NodeType = TypeVar("NodeType")


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

        books = await info.context.loaders.books_by_author.load(self.id)
        return [book_to_type(b) for b in books] if books else []


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
    async def book(self, info: Info) -> Optional[BookType]:
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
class UserProfileType:
    id: strawberry.ID
    email: Optional[str]
    name: Optional[str]
    username: Optional[str]
    fullname: Optional[str]
    rol: Optional[str] = strawberry.field(permission_classes=[RBAC("admin")])
    second_name: Optional[str]
    street_adress: Optional[str]
    city: Optional[str]
    province: Optional[str]
    zip_code: Optional[str]
    about: Optional[str]


@strawberry.type
class LoginResponse:
    access_token: str
    refresh_token: str
    token_type: str
    user: Optional[UserType] = None


@strawberry.type
class CustomPageInfo(strawberry.relay.PageInfo):
    """PageInfo extended with aditional info"""

    total_count: int


@strawberry.type
class AuthorConnection:
    page_info: CustomPageInfo
    edges: list[strawberry.relay.Edge[AuthorType]]


@strawberry.type
class ConferenceRoomType:
    id: strawberry.ID
    name: str
    capacity: int
    price_per_hour: float
    is_active: bool

    @strawberry.field
    async def available_hours(self, starting_hour: int, info: Info) -> List[int]:
        return await info.context.loaders.room_hours.load((int(self.id), starting_hour))


@strawberry.type
class RoomBookingType:
    id: strawberry.ID
    user_id: Optional[int] = None
    room_id: int
    attendees_count: int
    hour: int
    status: str
    date: str
