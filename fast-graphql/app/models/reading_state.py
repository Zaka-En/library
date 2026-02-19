from app.database import Base
from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

if TYPE_CHECKING:
  from .book import Book
  from .user import User


class ReadingState(Base):

  __tablename__ = "reading_states"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True
  )

  book_id: Mapped[int] = mapped_column(
    ForeignKey('books.id'),
    nullable=False
  )

  user_id: Mapped[int] = mapped_column(
    
    ForeignKey("users.id"),
    nullable=False
  )

  current_page: Mapped[int] = mapped_column(
    Integer,
    nullable=False
  )

  start_date: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    nullable=False
  )

  finish_date: Mapped[Optional[datetime]] = mapped_column(
    DateTime,
    nullable=True
  )

  book: Mapped["Book"] = relationship(
    "Book",
    back_populates="reading_states"
  )

  user: Mapped["User"] = relationship(
    "User",
    back_populates="reading_states"
  )
 



