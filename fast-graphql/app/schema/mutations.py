from .inputs import ( CreateAuthorInput, UpdateAuthorInput, CreateBookInput, UpdateBookInput, StartReadingInput, UpdateProgressInput, FinishReadingInput )
from .types import AuthorType, BookType, ReadingStateType
import strawberry
from strawberry.types import Info
from app.models.author import Author
from app.models.book import Book
from app.models.reading_state import ReadingState
from .convertors import *
from datetime import datetime


@strawberry.type
class Mutation:

  @strawberry.mutation
  def create_author(self, input: CreateAuthorInput, info: Info) -> AuthorType:
    session = info.context['db']

    author = Author(
      name=input.name,
      biography=input.biography,
      fullname=input.fullname,
      country=input.country
    )

    session.add(author)
    session.commit()
    session.refresh(author)

    return author_to_type(author)

  @strawberry.mutation
  def update_author(self, input: UpdateAuthorInput, info: Info) -> AuthorType:
    session = info.context['db']
    
    author = session.query(Author).filter(Author.id == input.id).first()
    if not author:
      raise ValueError(f"Author with id {input.id} not found")
    
    
    input_dict = vars(input)
    
    for key, value in input_dict.items():
      if key != 'id' and value is not None:
        setattr(author, key, value)

    
    try:
      session.commit()
      session.refresh(author) # Para que el objeto author tenga los datos frescos de la DB
    except Exception as e:
      session.rollback()
      raise e
    
    return author_to_type(author)

  @strawberry.mutation
  def delete_author(self, id: int, info: Info) -> bool:
    session = info.context['db']
    
    author = session.query(Author).filter(Author.id == id).first()
    if not author:
      return False
    
    session.delete(author)
    session.commit()
    return True

  @strawberry.mutation
  def create_book(self, input: CreateBookInput, info: Info) -> BookType:
    session = info.context['db']
    
    book = Book(
      title=input.title,
      isbn=input.isbn,
      publication_year=input.publication_year,
      pages=input.pages,
      author_id=input.author_id
    )
    
    session.add(book)
    session.commit()
    session.refresh(book)
    
    return book_to_type(book)

  @strawberry.mutation
  def update_book(self, input: UpdateBookInput, info: Info) -> BookType:
    session = info.context['db']
    
    book = session.query(Book).filter(Book.id == input.id).first()
    if not book:
      raise ValueError(f"Book with id {input.id} not found")
    
   
    input_dict = vars(input)

    for key, value in input_dict.items():
      if key != 'id' and value is not None:
        setattr(book,key,value)
    
    session.commit()
    session.refresh(book)
    
    return book_to_type(book)

  @strawberry.mutation
  def delete_book(self, id: int, info: Info) -> bool:
    session = info.context['db']
    
    book = session.query(Book).filter(Book.id == id).first()
    if not book:
      return False
    
    session.delete(book)
    session.commit()
    return True

  @strawberry.mutation
  def start_reading(self, input: StartReadingInput, info: Info) -> ReadingStateType:
    session = info.context['db']
    
    # Validar que el libro existe
    book = session.query(Book).filter(Book.id == input.book_id).first()
    if not book:
      raise ValueError(f"Book with id {input.book_id} not found")
    
    reading_state = ReadingState(
      book_id=input.book_id,
      user_id=input.user_id,
      current_page=0
    )
    
    session.add(reading_state)
    session.commit()
    session.refresh(reading_state)
    
    return reading_state_to_type(reading_state)

  @strawberry.mutation
  def update_progress(self, input: UpdateProgressInput, info: Info) -> ReadingStateType:
    session = info.context['db']
    
    reading_state = session.query(ReadingState).filter(ReadingState.id == input.id).first()
    if not reading_state:
      raise ValueError(f"ReadingState with id {input.id} not found")
    
    # Validar que las páginas no son negativas
    if input.current_page < 0:
      raise ValueError("current_page cannot be negative")
    
    # Validar que no excede el total de páginas del libro
    book = session.query(Book).filter(Book.id == reading_state.book_id).first()
    if book and input.current_page > book.pages:
      raise ValueError(f"current_page ({input.current_page}) cannot exceed total pages ({book.pages})")
    
    reading_state.current_page = input.current_page
    
    session.commit()
    session.refresh(reading_state)
    
    return reading_state_to_type(reading_state)

  @strawberry.mutation
  def finish_reading(self, input: FinishReadingInput, info: Info) -> ReadingStateType:
    session = info.context['db']
    
    reading_state = session.query(ReadingState).filter(ReadingState.id == input.id).first()
    if not reading_state:
      raise ValueError(f"ReadingState with id {input.id} not found")
    
    reading_state.finish_date = datetime.now()
    
    session.commit()
    session.refresh(reading_state)
    
    return reading_state_to_type(reading_state)