# services/room_booking_service.py
from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.models.room_booking import RoomBooking
from .base import BaseService, SingletonService
from datetime import date

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

  async def create(
    self,
    data: dict
    ) -> RoomBooking:

    async with self.session_factory() as session:
      try:
        booking = RoomBooking(**data)
        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking
      except IntegrityError as e:

        if e.orig and hasattr(e.orig, 'args') and len(e.orig.args) > 1:
          error_code = e.orig.args[0]
          error_msg = e.orig.args[1]      

        if error_code == 1062: #UNIQUE CONSTR VIOLATION code
          if "uq_hour_room_date_booking" in error_msg:
            raise Exception("DUPLICATE_ROOM_BOOKING")
          raise Exception("DUPLICATE_ENTRY")

        raise Exception("INTEGRITY_ERROR_GENERAL")
      except Exception as e:
        await session.rollback()
        raise e

    
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
  
  async def _check_availability(
      self, 
      room_id: int, 
      start: int, 
      end: int,
      date: date
  ) -> bool:
      """Método específico: verificar si la sala está disponible en la franja horaria especificada"""
      async with self.session_factory() as session:
          
        if start < 9 or end > 19 or start >= end:
          return False
        
        query = select(RoomBooking).where(
          RoomBooking.room_id == room_id,
          RoomBooking.date == date,
          RoomBooking.end_hour > start,
          RoomBooking.start_hour < end
        )

        result = await session.execute(query)
        count = list(result.scalar())

        return count == 0
  
  async def get_available_slots(self, room_id: int , date: date) -> List[Tuple[int, int]]:

    async with self.session_factory() as session:
      ocuppied_slots_query = select(RoomBooking.start_hour, RoomBooking.end_hour).where(
        RoomBooking.date == date,
        RoomBooking.room_id == room_id,
        RoomBooking.status.in_(["pending", "confirmed"]),
      ).order_by(RoomBooking.start_hour)
      
      ocuppied_slots= list(await session.execute(ocuppied_slots_query))
      n = len(ocuppied_slots)
      available_slots : List[Tuple[int, int]] = []
      start_hour = 9
      end_hour = 19

      if n == 0:
        available_slots.append((start_hour,end_hour))
        return available_slots
      
      for index,row in enumerate(ocuppied_slots):
        current_start_hour_row = row[0]
        current_end_hour_row = row[1]
        if start_hour < current_start_hour_row:
          available_slots.append((start_hour,current_start_hour_row))

        start_hour = current_end_hour_row

        if index == n-1 and start_hour < end_hour:
          available_slots.append((start_hour,end_hour))

      return available_slots      
    
  async def get_available_hours(self, room_id: int , date: date) -> List[int]:
    async with self.session_factory() as session:
      booked_hours_query = select(RoomBooking.hour).where(
        RoomBooking.date == date,
        RoomBooking.room_id == room_id,
        RoomBooking.status.in_(["pending", "confirmed"]),
      ).order_by(RoomBooking.hour)

      result = await session.execute(booked_hours_query)
      booked_hours = result.scalars().all()

      FIRST_AVAILABLE_HOUR = 9
      LAST_AVAILABLE_HOUR = 18
      HOURS_RANGE = range(FIRST_AVAILABLE_HOUR,LAST_AVAILABLE_HOUR + 1)
    
      if len(booked_hours) == 0:
        return list(HOURS_RANGE)
      
      return [hour for hour in HOURS_RANGE if hour not in booked_hours ] 

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