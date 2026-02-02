from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .types import *


def author_to_type(author: Author) -> AuthorType:
  return AuthorType(
    id=author.id,
    name=author.name,
    biography=author.biography,
    country=author.country,
    fullname=author.fullname
  )

def book_to_type(book: Book) -> BookType:
  return BookType(
    id=book.id,
    title=book.title,
    isbn=book.isbn,
    publication_year=book.publication_year,
    pages=book.pages,
    author_id=book.author_id
  )

def reading_state_to_type(state: ReadingState) -> ReadingStateType:
  return ReadingStateType(
      id=state.id,
      current_page=state.current_page,
      start_date=state.start_date,
      finish_date=state.finish_date,
      book_id=state.book_id
  )