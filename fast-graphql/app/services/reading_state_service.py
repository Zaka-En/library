from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.models.reading_state import ReadingState
from app.models.book import Book

class ReadingStateService():
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
    if not hasattr(self, "session_factory"):
      self.session_factory = session_factory

  async def get_user_progress(self, user_id: int) -> List[ReadingState]:
    async with self.session_factory() as session:
      query = select(ReadingState).filter(
        ReadingState.user_id == user_id,
        ReadingState.finish_date.is_(None)
      )
      result = await session.execute(query)
      return list(result.scalars().all())

  async def get_by_id(self, id: int) -> ReadingState:
    async with self.session_factory() as session:
      query = select(ReadingState).filter(ReadingState.id == id)
      result = await session.execute(query)
      return result.scalar_one_or_none()

  async def finish_reading(self, state_id: int) -> Optional[ReadingState]:
    async with self.session_factory() as session:
      result = await session.execute(select(ReadingState).filter(ReadingState.id == state_id))
      state = result.scalar_one_or_none()
      if not state:
        return None
      state.finish_date = datetime.now()
      await session.commit()
      await session.refresh(state)
      return state

  async def update_progress(self, state_id: int, current_page: int) -> ReadingState:
    async with self.session_factory() as session:
      result = await session.execute(select(ReadingState).filter(ReadingState.id == state_id))
      state = result.scalar_one_or_none()
      if not state:
        raise ValueError(f"ReadingState with id {state_id} not found")
      if current_page < 0:
        raise ValueError("current_page cannot be negative")
      result_book = await session.execute(select(Book).filter(Book.id == state.book_id))
      book = result_book.scalar_one_or_none()
      if book and current_page > book.pages:
        raise ValueError(f"current_page ({current_page}) cannot exceed total pages ({book.pages})")
      state.current_page = current_page
      await session.commit()
      await session.refresh(state)
      return state

  async def start_reading(self, book_id: int, user_id: int, current_page: int = 1) -> ReadingState:
    async with self.session_factory() as session:
      result_book = await session.execute(select(Book).filter(Book.id == book_id))
      book = result_book.scalar_one_or_none()
      if not book:
        raise ValueError(f"Book with id {book_id} not found")
      if current_page < 0:
        raise ValueError("Current page cannot be negative")
      if current_page > book.pages:
        raise ValueError(f"Current page ({current_page}) cannot exceed total pages ({book.pages})")
      active_reading = await session.execute(
        select(ReadingState).filter(
          ReadingState.user_id == user_id,
          ReadingState.book_id == book_id,
          ReadingState.finish_date.is_(None)
        )
      )
      if active_reading.scalar_one_or_none():
        raise ValueError("You already have an active reading session for this book")
      new_reading_state = ReadingState(
        book_id=book_id,
        user_id=user_id,
        current_page=current_page,
        start_date=datetime.now()
      )
      session.add(new_reading_state)
      await session.commit()
      await session.refresh(new_reading_state)
      return new_reading_state