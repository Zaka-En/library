import strawberry
from typing import List, Optional
from strawberry.types import Info
from .types import AuthorType, BookType, ReadingStateType
from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .convertors import *


@strawberry.type
class Query:
  
  @strawberry.field
  def authors(self, info: Info) -> List[AuthorType]:
    session = info.context['db']
    authors = session.query(Author).all()
    return [author_to_type(author) for author in authors]

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


