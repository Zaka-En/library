import strawberry
from typing import List, Optional
from strawberry.types import Info
from .types import AuthorType, BookType, ReadingStateType, CustomPageInfo, AuthorConnection
from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .convertors import *
from strawberry import relay
from typing import  AsyncGenerator, Tuple
import asyncio
from datetime import datetime
from app.services.author_service import AuthorService
# from app.services.book_service import BookService
from app.services.reading_state_service import ReadingStateService


VALORACIONES = [
  "Increíble historia, me encantó",
  "Un poco lento al principio",
  "Los personajes son muy profundos",
  "No entendí el final",
  "Obra maestra contemporánea"
]



@strawberry.type
class Query:

  @strawberry.field
  async def authors_query (self, info: Info) -> List[AuthorType]:
    author_service: AuthorService = info.context["author_service"]
    authors = await author_service.get_all()
    return [author_to_type(a) for a in authors]

  @strawberry.field
  async def authors(
    self,
    info: Info,
    first: Optional[int] = None, 
    after: Optional[str] = None
    ) -> AuthorConnection:

    author_service: AuthorService = info.context["author_service"]
    
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

  @strawberry.field
  async def author(self, id: int, info: Info) -> Optional[AuthorType]:
    author_service: AuthorService = info.context["author_service"]
    author = await author_service.get_by_id(id)
    return author_to_type(author) if author else None

  @strawberry.field
  async def books(self, info: Info) -> List[BookType]:
    book_service = info.context["book_service"]
    books = await book_service.get_all()
    return [book_to_type(b) for b in books]

  @strawberry.field
  async def book(self, id: int, info: Info) -> Optional[BookType]:
    book_service = info.context["book_service"]
    book: Book = await book_service.get_by_id(book_id=id)
    return book_to_type(book) if book else None

  @strawberry.field
  async def my_reading_progress(self, user_id: int, info: Info) -> List[ReadingStateType]:
    service: ReadingStateService = info.context["reading_state_service"]
    reading_states = await service.get_user_progress(user_id=user_id)

    return [reading_state_to_type(r) for r in reading_states]

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