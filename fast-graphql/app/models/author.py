from app.database import Base
from typing import Optional, List
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Author(Base):

  __tablename__ = "authors"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True
  )

  name: Mapped[str] = mapped_column(
    String(50),
    nullable=False
  )

  fullname: Mapped[Optional[str]] = mapped_column(
    String(100),
    nullable=True
  )

  biography: Mapped[Optional[str]] = mapped_column(
    Text,
    nullable=True
  )

  country: Mapped[str] = mapped_column(
    String(30),
    nullable=False
  )

  # Relación con Book
  books: Mapped[List["Book"]] = relationship(
    "Book",
    back_populates="author",
    cascade="all, delete-orphan"
  )