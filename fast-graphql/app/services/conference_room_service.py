from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.models.conference_room import ConferenceRoom
from .base import BaseService, SingletonService

class ConferenceRoomService(BaseService[ConferenceRoom], SingletonService):
  def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
    self.session_factory = session_factory
  
  async def get_by_id(self, id: int) -> Optional[ConferenceRoom]:
    async with self.session_factory() as session:
      result = await session.execute(
        select(ConferenceRoom).where(ConferenceRoom.id == id)
      )
      return result.scalar_one_or_none()
  
  async def get_all(self) -> List[ConferenceRoom]:
    async with self.session_factory() as session:
      result = await session.execute(select(ConferenceRoom))
      return list(result.scalars().all())
  
  async def get_by_ids(self, ids: List[int]) -> List[ConferenceRoom]:
    async with self.session_factory() as session:
      result = await session.execute(
        select(ConferenceRoom).where(ConferenceRoom.id.in_(ids))
      )
      return list(result.scalars().all())
  
  async def create(self, data: dict) -> ConferenceRoom:
    async with self.session_factory() as session:
      room = ConferenceRoom(**data)
      session.add(room)
      await session.commit()
      await session.refresh(room)
      return room
  
  async def update(self, data: dict) -> ConferenceRoom:
    async with self.session_factory() as session:
      result = await session.execute(
        select(ConferenceRoom).where(ConferenceRoom.id == data["id"])
      )
      room = result.scalar_one_or_none()
      
      if not room:
        raise ValueError(f"ConferenceRoom with id {data['id']} not found")
      
      for key, value in data.items():
        if key != "id" and hasattr(room, key):
            setattr(room, key, value)
    
      await session.commit()
      await session.refresh(room)
      return room
  
  async def delete(self, id: int) -> ConferenceRoom:
    async with self.session_factory() as session:
      result = await session.execute(
        select(ConferenceRoom).where(ConferenceRoom.id == id)
      )
      room = result.scalar_one_or_none()
      
      if not room:
        raise ValueError(f"ConferenceRoom with id {id} not found")
      
      await session.execute(
        delete(ConferenceRoom).where(ConferenceRoom.id == id)
      )
      await session.commit()
      return room
  
  async def get_active_rooms(self) -> List[ConferenceRoom]:
    """Method to get active rooms"""
    async with self.session_factory() as session:
      result = await session.execute(
          select(ConferenceRoom).where(ConferenceRoom.is_active == True)
      )
      return list(result.scalars().all())