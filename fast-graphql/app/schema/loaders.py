from strawberry.dataloader import DataLoader
from typing import List, Optional, Tuple
from app.services.book_service import BookService
from app.services.author_service import AuthorService
from app.services.room_booking_service import RoomBookingService
from app.models.book import Book
from app.models.author import Author
from dataclasses import dataclass
from datetime import date
import asyncio


#---------------Data Loaders-------------------
@dataclass
class DataLoaders:
  book: DataLoader[int, Optional[Book]]
  author: DataLoader[int, Optional[Author]]
  books_by_author: DataLoader[int, List[Book]]
  room_slots: DataLoader[int, List[Tuple[int, int]]]

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

async def load_available_slots_by_room_ids(
    
  room_ids: List[int],
  room_booking_service: RoomBookingService,
  target_date: date
  ) -> List[List[Tuple[int,int]]]:
  """Takes list of room ids and retreives availables slots of eahc room_id that same date"""
  
  tasks = [room_booking_service.get_available_slots(
    room_id=rid,
    date=target_date
    ) for rid in room_ids]
  
  results = await asyncio.gather(*tasks)

  return list(results)

  


def create_loaders(
  book_service: BookService,
  author_service: AuthorService, 
  room_booking_service: RoomBookingService
  ) -> DataLoaders:

  async def load_books(ids: List[int]) -> List[Optional[Book]]:
    return await load_books_by_ids(ids, book_service)

  async def load_authors(ids: List[int]) -> List[Optional[Author]]:
    return await load_authors_by_ids(ids, author_service)

  async def load_books_by_author(ids: List[int]) -> List[List[Book]]:
    return await load_books_by_author_ids(ids, book_service)
  
  async def load_slots(ids: List[int]) -> List[List[Tuple[int,int]]]:
    #date: hard-coded today's date to 
    return await load_available_slots_by_room_ids(room_ids=ids,room_booking_service=room_booking_service,target_date=date.today())

  return DataLoaders(
    book=DataLoader(load_fn=load_books),
    author=DataLoader(load_fn=load_authors),
    books_by_author=DataLoader(load_fn=load_books_by_author),
    room_slots=DataLoader(load_fn=load_slots)
  )

  