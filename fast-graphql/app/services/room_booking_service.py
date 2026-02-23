# services/room_booking_service.py
from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.models.room_booking import RoomBooking
from .base import BaseService, SingletonService

class RoomBookingService(BaseService[RoomBooking], SingletonService):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
      self.session_factory = session_factory
    
    async def get_by_id(self, id: int) -> Optional[RoomBooking]:
      async with self.session_factory() as session:
        result = await session.execute(
            select(RoomBooking).where(RoomBooking.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[RoomBooking]:
      async with self.session_factory() as session:
        result = await session.execute(select(RoomBooking))
        return list(result.scalars().all())
    
    async def get_by_ids(self, ids: List[int]) -> List[RoomBooking]:
      async with self.session_factory() as session:
        result = await session.execute(
            select(RoomBooking).where(RoomBooking.id.in_(ids))
        )
        return list(result.scalars().all())
  
    async def create(self, data: dict) -> RoomBooking:
      async with self.session_factory() as session:
        booking = RoomBooking(**data)
        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking
    
    async def update(self, data: dict) -> RoomBooking:
      async with self.session_factory() as session:
        result = await session.execute(
          select(RoomBooking).where(RoomBooking.id == data["id"])
        )
        booking = result.scalar_one_or_none()
        
        if not booking:
          raise ValueError(f"RoomBooking with id {data['id']} not found")
        
        for key, value in data.items():
          if key != "id" and hasattr(booking, key):
            setattr(booking, key, value)
        
        await session.commit()
        await session.refresh(booking)
        return booking
    
    async def delete(self, id: int) -> RoomBooking:
      async with self.session_factory() as session:
        result = await session.execute(
          select(RoomBooking).where(RoomBooking.id == id)
        )
        booking = result.scalar_one_or_none()
        
        if not booking:
          raise ValueError(f"RoomBooking with id {id} not found")
        
        await session.execute(
          delete(RoomBooking).where(RoomBooking.id == id)
        )
        await session.commit()
        return booking
    
    async def check_availability(
        self, 
        room_id: int, 
        start: datetime, 
        end: datetime,
        exclude_booking_id: Optional[int] = None
    ) -> bool:
        """Método específico: verificar si la sala está disponible"""
        async with self.session_factory() as session:
            query = select(RoomBooking).where(
                RoomBooking.room_id == room_id,
                RoomBooking.status.in_(["pending", "confirmed"]),
                or_(
                    and_(
                        RoomBooking.start_datetime <= start,
                        RoomBooking.end_datetime > start
                    ),
                    and_(
                        RoomBooking.start_datetime < end,
                        RoomBooking.end_datetime >= end
                    ),
                    and_(
                        RoomBooking.start_datetime >= start,
                        RoomBooking.end_datetime <= end
                    )
                )
            )
            
            if exclude_booking_id:
                query = query.where(RoomBooking.id != exclude_booking_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is None
    
    async def get_by_user(self, user_id: int) -> List[RoomBooking]:
      """Método específico: obtener reservas de un usuario"""
      async with self.session_factory() as session:
        result = await session.execute(
          select(RoomBooking).where(RoomBooking.user_id == user_id)
        )
        return list(result.scalars().all())
  
    async def get_by_room(self, room_id: int) -> List[RoomBooking]:
      """Método específico: obtener reservas de una sala"""
      async with self.session_factory() as session:
        result = await session.execute(
            select(RoomBooking).where(RoomBooking.room_id == room_id)
        )
        return list(result.scalars().all())