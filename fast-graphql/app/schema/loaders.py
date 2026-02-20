from strawberry.dataloader import DataLoader
from typing import List, Optional
from app.services.book_service import BookService
from app.services.author_service import AuthorService
from app.models.book import Book
from app.models.author import Author
from dataclasses import dataclass


#---------------Data Loaders-------------------
@dataclass
class DataLoaders:
  def __init__(self,book_loader,author_loader,books_by_author_loader):
    self.book = DataLoader(load_fn=book_loader) 
    self.author = DataLoader(load_fn=author_loader)
    self.books_by_author = DataLoader(load_fn=books_by_author_loader)


async def load_books_by_ids(book_ids: List[int], book_service: BookService) -> List[Optional[Book]]:
  books = await book_service.get_by_ids(book_ids)
  book_map = {b.id: b for b in books}
  return [book_map.get(id) for id in book_ids]


async def load_authors_by_ids(author_ids: List[int], author_service: AuthorService) -> List[Optional[Author]]:
  authors = await author_service.get_by_ids(author_ids)
  author_map = {a.id: a for a in authors}
  return [author_map.get(id) for id in author_ids]

async def load_books_by_author_ids(author_ids: List[int], book_service: BookService) -> List[List[Book]]:
  books = await book_service.get_by_author_ids(author_ids)
  books_by_author: dict[int, List] = {id: [] for id in author_ids}
  for book in books:
    books_by_author[book.author_id].append(book)
  return [books_by_author[id] for id in author_ids]


def create_loaders(book_service: BookService, author_service: AuthorService) -> DataLoaders:

  async def load_books(ids: List[int]) -> List[Optional[Book]]:
    return await load_books_by_ids(ids, book_service)

  async def load_authors(ids: List[int]) -> List[Optional[Author]]:
    return await load_authors_by_ids(ids, author_service)

  async def load_books_by_author(ids: List[int]) -> List[List[Book]]:
    return await load_books_by_author_ids(ids, book_service)

  return DataLoaders(
    book_loader=load_books,
    author_loader=load_authors,
    books_by_author_loader=load_books_by_author
  )

  