import strawberry
from typing import List, Optional
from strawberry.types import Info
from .types import AuthorType, BookType, ReadingStateType, CustomPageInfo, AuthorConnection, UserProfileType
from app.models.book import Book
from .convertors import reading_state_to_type, book_to_type, author_to_type
from strawberry import relay
from typing import Tuple
import asyncio
from datetime import datetime
from app.services.author_service import AuthorService
# from app.services.book_service import BookService
from app.services.reading_state_service import ReadingStateService
from app.utils.permissions import IsAuthenticated
from app.models.user import User
from app.dependencies import CustomContext
from app.utils.permissions import RBAC


VALORACIONES = [
  "Increíble historia, me encantó",
  "Un poco lento al principio",
  "Los personajes son muy profundos",
  "No entendí el final",
  "Obra maestra contemporánea"
]

@strawberry.type
class Query:

  #TODO add a permission: isuserowner
  @strawberry.field #(permission_classes=[IsAuthenticated])
  async def user_info(self, info: Info[CustomContext, None], user_id: int) -> UserProfileType :

    user_from_payload = info.context.user

    # if not user_from_payload or not user_from_payload["id"] != user_id:
    #   raise Exception("CAN NOT QUERY OR MODIFY OTHERS PRFILES")
    

    service = info.context.user_service
    user: User = await service.get_all_info_by_id(user_id)
    print("="*90)
    print("DEBUG USER PROFILE", vars(user))
    print("="*90)
    return UserProfileType(
      id=strawberry.ID(str(user.id)),
      email=user.email,
      name=user.name,
      username=user.username,
      fullname=user.fullname,
      rol=user.rol,
      second_name=user.second_name,
      street_adress=user.street_adress,
      city=user.city,
      province=user.province,
      zip_code=user.zip_code,
      about=user.about
    )

  @strawberry.field
  async def authors_query (self, info: Info[CustomContext, None]) -> List[AuthorType]:
    author_service: AuthorService = info.context.author_service
    authors = await author_service.get_all()
    return [author_to_type(a) for a in authors]

  @strawberry.field
  async def authors(
    self,
    info: Info,
    first: Optional[int] = None, 
    after: Optional[str] = None
    ) -> AuthorConnection:

    author_service: AuthorService = info.context.author_service
    
    result = await author_service.get_paginated(
      limit=first or 5, 
      after_cursor=after
    )

    edges = [
      relay.Edge(
          node=author_to_type(author),
          cursor=author_service._encode_cursor(author.id)
      ) for author in result.items
    ]

    return AuthorConnection(
      edges=edges,
      page_info= CustomPageInfo(
        has_previous_page=False,
        has_next_page=result.has_next_page,
        end_cursor=result.end_cursor,
        start_cursor=result.start_cursor,
        total_count=len(edges)
      )
    )


  @strawberry.field(permission_classes=[RBAC("admin")])
  async def author(self, id: int, info: Info[CustomContext, None]) -> Optional[AuthorType]:
    author_service: AuthorService = info.context.author_service
    author = await author_service.get_by_id(id)
    return author_to_type(author) if author else None

  @strawberry.field
  async def books(self, info: Info[CustomContext, None]) -> List[BookType]:
    book_service = info.context.book_service
    books = await book_service.get_all()
    return [book_to_type(b) for b in books]

  @strawberry.field
  async def book(self, id: int, info: Info[CustomContext, None]) -> Optional[BookType]:
    book_service = info.context.book_service
    book: Book = await book_service.get_by_id(book_id=id)
    return book_to_type(book) if book else None

  @strawberry.field
  async def my_reading_progress(self, user_id: int, info: Info[CustomContext, None]) -> List[ReadingStateType]:
    service: ReadingStateService = info.context.reading_state_service
    reading_states = await service.get_user_progress(user_id=user_id)

    return [reading_state_to_type(r) for r in reading_states]

  #TODO: user is no longer just a string
  @strawberry.field
  async def recomendations(self, user: str) -> Tuple[str,str,str]: 

    async def recomender(service: str):
      await asyncio.sleep(2)
      return f"Libro recomendado {service}"

    start = datetime.now()

    results = await asyncio.gather(
      recomender("Drama"),
      recomender("Horror"),
      recomender("Sitcom")
    )

    diff = datetime.now() - start

    print(f"Tiempo total: {diff.seconds} segundos") # Debería ser ~2s, no 6s

    return results