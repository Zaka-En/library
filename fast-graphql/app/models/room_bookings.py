from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, DateTime, CheckConstraint
from datetime import datetime

if TYPE_CHECKING:
  from .user import User
  from .conference_room import ConferenceRoom


class RoomBooking(Base):

  __tablename__ = "room_bookings"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True
  )

  user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True
  )

  room_id: Mapped[int] = mapped_column(
    ForeignKey("conference_rooms.id"),
    nullable=True
  )

  start_datetime: Mapped[datetime] = mapped_column(
    type_=DateTime,
    nullable=True
  )

  end_datetime: Mapped[datetime] = mapped_column(
    type_=DateTime,
    nullable=True
  )

  attendees_count = mapped_column(
    Integer,
    nullable=False
  )

  status: Mapped[str]  = mapped_column(
    String(10),
    default="pending"
  )

  user: Mapped["User"] = relationship(
    back_populates="room_bookings",
    passive_deletes=True
  )

  room: Mapped["ConferenceRoom"] = relationship(
    back_populates="room_bookings",
    passive_deletes=True
  )

  #-----Constraints-------
  __table_args__ = (
    CheckConstraint(sqltext='start_datetime < end_datetime' , name="check_user_role"),
  )

