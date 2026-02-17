# app/services/reading_state_service.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reading_state import ReadingState
from app.models.book import Book

class ReadingStateService():
  def __init__(self, session: AsyncSession):
    self.session = session

  async def get_user_progress(self, user_id: int) -> List[ReadingState]:
      
    query = select(ReadingState).filter(
      ReadingState.user_id == user_id,
      ReadingState.finish_date == None
    )
    result = await self.session.execute(query)
    return list(result.scalars().all())


  async def get_by_id(self, id: int) -> ReadingState:
    query = select(ReadingState).filter(
      ReadingState.id == id
    )
    result = await self.session.execute(query)
    return result.scalar_one_or_none()
  

  async def finish_reading(self, state_id: int) -> Optional[ReadingState]:
      
    state = await self.get_by_id(state_id)
    if not state:
      return None
    
    state.finish_date = datetime.now()
    await self.session.commit()
    await self.session.refresh(state)
    return state
  

  async def update_progress(self, state_id: int, current_page: int) -> ReadingState:
  
    state = await self.get_by_id(state_id)
    if not state:
      raise ValueError(f"ReadingState with id {state_id} not found")
    
    
    if current_page < 0:
      raise ValueError("current_page cannot be negative")
    
    from app.models.book import Book 
    result_book = await self.session.execute(select(Book).filter(Book.id == state.book_id))
    book = result_book.scalar_one_or_none()
    
    if book and current_page > book.pages:
      raise ValueError(f"current_page ({current_page}) cannot exceed total pages ({book.pages})")
    

    state.current_page = current_page
    
    await self.session.commit()
    await self.session.refresh(state)
    
    return state

  async def start_reading(self, book_id: int, user_id: int, current_page: int = 1) -> ReadingState:
    
    result_book = await self.session.execute(
      select(Book).filter(Book.id == book_id)
    )
    book = result_book.scalar_one_or_none()
    
    if not book:
      raise ValueError(f"Book with id {book_id} not found")
    
    
    if current_page < 0:
      raise ValueError("Current page cannot be negative")
    if current_page > book.pages:
      raise ValueError(f"Current page ({current_page}) cannot exceed total pages ({book.pages})")

    # 3. Evitar duplicados (opcional: verificar si ya hay una lectura activa para este libro)
    query_active = select(ReadingState).filter(
      ReadingState.user_id == user_id,
      ReadingState.book_id == book_id,
      ReadingState.finish_date == None
    )
    active_reading = await self.session.execute(query_active)

    if active_reading.scalar_one_or_none():
      raise ValueError("You already have an active reading session for this book")

    
    new_reading_state = ReadingState(
      book_id=book_id,
      user_id=user_id,
      current_page=current_page,
      start_date=datetime.now()
    )
    
    self.session.add(new_reading_state)
    await self.session.commit()
    await self.session.refresh(new_reading_state)
    
    return new_reading_state
  