from app.database import Base
from sqlalchemy import String, Integer, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from .room_booking import RoomBooking

class ConferenceRoom(Base):

  __tablename__ = "conference_rooms"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True
  )

  name: Mapped[str] = mapped_column(
    String(50),
    nullable=True
  )

  capacity: Mapped[int] = mapped_column(
    type_=Integer,
    nullable=False
  )

  price_per_hour: Mapped[float] = mapped_column(
    type_=Numeric(10,2),
    nullable=True
  )

  is_active: Mapped[bool] = mapped_column(
    type_=Boolean,
    nullable=True
  )


  room_bookings: Mapped[List["RoomBooking"]]  = relationship( back_populates="room")


