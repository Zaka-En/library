import strawberry
from typing import List, Optional
from strawberry.types import Info
from .types import AuthorType, BookType, ReadingStateType
from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .convertors import *
from strawberry import relay
import base64


@strawberry.type
class Query:

  @strawberry.field
  def authors_query (self, info: Info) -> List[AuthorType]:
    session = info.context['db']
    authors = session.query(Author).all()
    return [author_to_type(author) for author in authors]
  
  @strawberry.field
  def authors(self, info: Info, first: int = 5, after: Optional[str]=None)-> relay.Connection[AuthorType]:
    session = info.context['db']
    
    query = session.query(Author).order_by(Author.id)
    all_authors = query.all()

    start_index = 0
    if after:
      try:
        decoded_cursor = base64.b64decode(after).decode().split(':')[-1]
        after_id = int(decoded_cursor)
        start_index = next(i + 1 for i, a in enumerate(all_authors) if a.id == after_id)
      except Exception :
        start_index = 0

    end_index = start_index + first
    authors_to_retrive = [ author_to_type(a) for a in all_authors[start_index:end_index]]

    edges = [
      relay.Edge(node=author, cursor=base64.b64encode(f"arrayconnection:{author.id}".encode()).decode())
      for author in authors_to_retrive
    ]

    has_next_page = len(all_authors) > end_index
    has_previous_page = start_index > 0

    return relay.Connection(
      edges=edges,
      page_info=relay.PageInfo(
        start_cursor=edges[0].cursor if edges else None,
        end_cursor=edges[-1].cursor if edges else None,
        has_next_page=has_next_page,
        has_previous_page=has_previous_page,
      )
    )
    


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


