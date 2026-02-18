# app/services/book_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.book import Book
from app.models.author import Author
from typing import Sequence, Optional, List
from app.schema.inputs import CreateBookInput, UpdateBookInput



class BookService:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def get_all(self) -> Sequence[Book]:
    
    result = await self.session.execute(select(Book))
    return result.scalars().all()

  async def get_by_id(self, book_id: int) -> Book:
    result = await self.session.execute(select(Book).filter(Book.id == book_id))
    return result.scalar_one_or_none()
  
  async def get_by_ids(self, books_ids: list[int]) -> List[Book]:
    return list((await self.session.execute(select(Book).where(Author.id.in_(books_ids)))).scalars().all())
  
  async def get_by_author_ids(self, authors_ids: list[int]) ->  List[Book]:
    return list((await self.session.execute(select(Book).where(Book.author_id.in_(authors_ids)))).scalars().all())

  async def create(self, input: CreateBookInput):
    
    author_check = await self.session.execute(select(Author).filter(Author.id == input.author_id))
    if not author_check.scalar_one_or_none():
      raise ValueError(f"No se puede crear el libro: El autor {input.author_id} no existe")
    
    IsbnQuery = await self.session.execute(select(Book).filter(Book.isbn == input.isbn))
    isbnAlreadyExists = IsbnQuery.scalar_one_or_none()

    if isbnAlreadyExists:
      raise Exception("UNIQUE ISBN RULE VIOLATED")   
    elif len(input.isbn) < 13:
      raise  Exception("INVALID ISBN: exactly 13 characters")   

    new_book: Book = Book(
      title=input.title,
      isbn=input.isbn,
      author_id=input.author_id,
      publication_year=input.publication_year,
      pages=input.pages
    )

    self.session.add(new_book)
    await self.session.commit()
    await self.session.refresh(new_book)
    return new_book
  
  async def update(self, input: UpdateBookInput) -> Optional[Book]:
    book = await self.get_by_id(input.id)
    if not book:
      return None
    
    
    input_dict = vars(input)
    for key, value in input_dict.items():
      if key != 'id' and value is not None:
        setattr(book, key, value)
    
    await self.session.commit()
    await self.session.refresh(book)
    return book
  
  async def delete(self, id: int) -> bool:
    result = await self.session.execute(select(Book).filter(Book.id == id))
    book = result.scalar_one_or_none()
    if not book:
      return False
    
    await self.session.delete(book)
    await self.session.commit()

    return True
  
  async def get_by_author(self, author_id: int) -> List[Book]:
    query = select(Book).filter(Book.author_id == author_id)
    result = await self.session.execute(query)
    return list(result.scalars().all())