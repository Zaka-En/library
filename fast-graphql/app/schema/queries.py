import strawberry
from typing import List, Optional
from strawberry.types import Info
from .types import AuthorType, BookType, ReadingStateType, broadcast, CustomPageInfo, AuthorConnection
from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .convertors import *
from strawberry import relay
import base64
from sqlalchemy import select
from typing import  AsyncGenerator, Tuple
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


VALORACIONES = [
  "Increíble historia, me encantó",
  "Un poco lento al principio",
  "Los personajes son muy profundos",
  "No entendí el final",
  "Obra maestra contemporánea"
]


@strawberry.type
class Subscription:

  @strawberry.subscription
  async def book_ratings(self) -> AsyncGenerator[str, None]:
    async with broadcast.subscribe(channel="RATINGS") as subscriber:
      while True:
        event = await subscriber.get()
        yield event.message
  
  @strawberry.subscription
  async def update_author_notifications(self) -> AsyncGenerator[str, None]:
    async with broadcast.subscribe(channel="NOTIFICATIONS") as subscriber:
      while True:
        event = await subscriber.get()
        yield event.message

  @strawberry.subscription
  async def book_chat(self, book_id: int) -> AsyncGenerator[str,None] :
    channel = f"BOOK_CHAT_{book_id}"
    async with broadcast.subscribe(channel=channel) as subscriber:
      while True:
        event = await subscriber.get()
        print(f"PUBLISHED to all subscriber : {event.message}")
        yield event.message
    



@strawberry.type
class Query:

  @strawberry.field
  async def authors_query (self, info: Info) -> List[AuthorType]:
    async with info.context['db_factory']() as session:
      result = await session.execute(
        select(Author)
      )
      authors = result.scalars().all()
      return [author_to_type(author) for author in authors]

  @strawberry.field
  async def authors(
    self,
    info: Info,
    first: Optional[int] = None, 
    after: Optional[str] = None) -> AuthorConnection:

    async with info.context['db_factory']() as session:
      after_id = 0
      first = first if first else 5
      has_next_page = False

      if after:
        decoded_cursor = base64.b64decode(after).decode().split(':')[-1]
        after_id =  int(decoded_cursor)

      #este es generador, cada vez que hace un viaje hacia mariadb trae (first + 1) elementos 
      async def authors_generator( session: AsyncSession, first: int , after_id: int = 0 ):
        query = select(Author).order_by(Author.id)

        if after_id:
          query = query.filter(Author.id > after_id)

        query = query.limit(first + 1)
      
        result = await session.execute(query)

        for author in result.scalars():
          yield author

      authors_stream = authors_generator(session,first, after_id)

      async def edges_generator(stream, limit: int):
        nonlocal has_next_page
        i = 0
        async for author in stream:
          if i < limit:
            yield relay.Edge(
              node=author_to_type(author),
              cursor=base64.b64encode(f"arrayconnection:{author.id}".encode()).decode()
            )
            i += 1
          else:
            has_next_page = True
            return

      edges_gen= edges_generator(stream=authors_stream,limit=first)

      edges = [edge async for edge in edges_gen]

      end_cursor = edges[-1].cursor if edges else None
      start_cursor = edges[0].cursor if edges else None

      return AuthorConnection(
        edges=edges,
        page_info= CustomPageInfo(
          has_previous_page=False,
          has_next_page=has_next_page,
          end_cursor=end_cursor,
          start_cursor=start_cursor,
          total_count=len(edges)
        )
      )


  @strawberry.field
  async def author(self, id: int, info: Info) -> Optional[AuthorType]:
    async with info.context['db_factory']() as session:
      result = await session.execute(
          select(Author).filter(Author.id == id)
      )
      author = result.scalar_one_or_none()
      return author_to_type(author) if author else None

  @strawberry.field
  async def books(self, info: Info) -> List[BookType]:
    async with info.context['db_factory']() as session:
      result = await session.execute(select(Book))
      books = result.scalars().all()
      return [book_to_type(book) for book in books]

  @strawberry.field
  async def book(self, id: int, info: Info) -> Optional[BookType]:
    async with info.context['db_factory']() as session:
      result = await session.execute(
          select(Book).filter(Book.id == id)
      )
      book = result.scalar_one_or_none()
      return book_to_type(book) if book else None

  @strawberry.field
  async def my_reading_progress(self, user_id: int, info: Info) -> List[ReadingStateType]:
    async with info.context['db_factory']() as session:
      result = await session.execute(
          select(ReadingState).filter(
              ReadingState.user_id == user_id,
              ReadingState.finish_date == None
          )
      )
      books_in_progress = result.scalars().all()
      return [reading_state_to_type(book) for book in books_in_progress]

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