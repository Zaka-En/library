import strawberry
from typing import List, Optional
from strawberry.types import Info
from .types import AuthorType, BookType, ReadingStateType, broadcast
from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .convertors import *
from strawberry import relay
import base64
from sqlalchemy.orm import Session
from typing import Generator, Any, AsyncGenerator
import asyncio
from broadcaster import Broadcast


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


@strawberry.type
class Query:

  @strawberry.field
  def authors_query (self, info: Info) -> List[AuthorType]:
    session = info.context['db']
    authors = session.query(Author).all()
    return [author_to_type(author) for author in authors]

  @staticmethod
  def authors_generator( session: Session, first: int , after_id: int = 0 ):
    query = session.query(Author).order_by(Author.id)

    if after_id:
      query = query.filter(Author.id > after_id)

    query = query.limit(first + 1).yield_per(first + 1)

    for author in query:
      yield author

  @strawberry.field
  def authors(
    self,
    info: Info,
    first: Optional[int] = None, 
    after: Optional[str] = None) -> AuthorConnection:

    session = info.context['db']
    after_id = 0
    first = first if first else 5
    has_next_page = False

    if after:
      decoded_cursor = base64.b64decode(after).decode().split(':')[-1]
      after_id =  int(decoded_cursor)

    #este es generador, cada vez que hace un viaje hacia mariadb trae (first + 1) elementos 
    authors_stream = Query.authors_generator(session,first, after_id)

    def edges_generator(stream: Generator[Author, Any, None], limit: int):
      nonlocal has_next_page
      for i, author in enumerate(stream):
        if i < limit:
          yield relay.Edge(
            node= author_to_type(author),
            cursor=base64.b64encode(f"arrayconnection:{author.id}".encode()).decode()
          )
        else:
          has_next_page=True
          return

    edges_gen= edges_generator(stream=authors_stream,limit=first)

    edges = list(edges_gen)

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


  """
  @strawberry.field
  def authors(
    self, info: Info, 
    first: Optional[int] = None, 
    last: Optional[int] = None, 
    after: Optional[str] = None, 
    before: Optional[str] = None) -> AuthorConnection:

    session = info.context['db']
      
    query = session.query(Author).order_by(Author.id).yield_per(first if first else 5)
    all_authors = query.all()

    start_index = 0
    total_count = end_index = len(all_authors)

    try:
      if after:
        decoded_cursor = base64.b64decode(after).decode().split(':')[-1]
        after_id = int(decoded_cursor)
        start_index = next((i + 1 for i, a in enumerate(all_authors) if a.id == after_id), 0)
        end_index = start_index + (first if first else 5)
      elif before:
        decoded_cursor = base64.b64decode(before).decode().split(':')[-1]
        before_id = int(decoded_cursor)
        end_index =  next((i for i, a in enumerate(all_authors) if a.id == before_id), 0)
        start_index = max(0, end_index - (last if last else 5)) 
      else: # this would happen the first time the data is retrieved  
        end_index = min(end_index, first if first else 5) 
    except Exception:
      start_index = 0


    authors_to_retrive = [ author_to_type(a) for a in all_authors[start_index:end_index]]

    edges = [
      relay.Edge(node=author, cursor=base64.b64encode(f"arrayconnection:{author.id}".encode()).decode())
      for author in authors_to_retrive
    ]

    has_next_page = len(all_authors) > end_index
    has_previous_page = start_index > 0

    return AuthorConnection(
      edges=edges,
      page_info=CustomPageInfo(
        start_cursor=edges[0].cursor if edges else None,
        end_cursor=edges[-1].cursor if edges else None,
        has_next_page=has_next_page,
        has_previous_page=has_previous_page,
        total_count=total_count
      )
    )
  """  


  @strawberry.field
  def author(self, id: int, info: Info) -> Optional[AuthorType]:
    session = info.context['db']
    author = session.query(Author).filter(Author.id == id).first()
    return author_to_type(author) if author else None

  @strawberry.field
  def books(self, info: Info) -> List[BookType]:
    session = info.context['db']
    books = session.query(Book).all()
    return [book_to_type(book) for book in books]  

  @strawberry.field
  def book(self, id: int, info: Info) -> Optional[BookType]:
    session = info.context['db']
    book = session.query(Book).filter(Book.id == id).first()
    return book_to_type(book) if book else None  

  @strawberry.field
  def my_reading_progress(self, user_id: str, info: Info) -> List[ReadingStateType]:
    session = info.context['db']
    books_in_progress = session.query(ReadingState).filter(ReadingState.user_id == user_id, ReadingState.finish_date == None)

    return [reading_state_to_type(book) for book in books_in_progress] 


