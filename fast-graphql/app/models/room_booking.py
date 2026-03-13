from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, CheckConstraint, Date, UniqueConstraint
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

  hour: Mapped[int] = mapped_column(
    Integer,
    nullable=False
  )

  date: Mapped[datetime] = mapped_column(
    Date,
    nullable=True
  )

  attendees_count = mapped_column(
    Integer,
    nullable=False
  )

  status: Mapped[str]  = mapped_column(
    String(10),
    default="pending" #confirmed canceled 
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
    CheckConstraint(sqltext='hour>=9 and hour<= 18', name='check_hour_between_9_and_18'),
    UniqueConstraint(
      "hour",
      "room_id",
      "date",
      name='uq_hour_room_date_booking'
    ),
  )
  # __table_args__ = (
  #   CheckConstraint(sqltext='start_hour < end_hour' , name="check_start_hour_<_end_hour"),
  #   CheckConstraint(sqltext='start_hour >= 8 AND end_hour <= 19', name='check_start_and_end_hours_in_range')
  # )




