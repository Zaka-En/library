from app.database import Base
from typing import List
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Book(Base):

  __tablename__ = "books"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True
  )

  isbn: Mapped[str] = mapped_column(
    String(13),
    unique=True,
    nullable=False
  )

  title: Mapped[str] = mapped_column(
    String(150),
    nullable=False
  ) 

  publication_year: Mapped[int] = mapped_column(
    Integer,
    nullable=False
  )

  pages: Mapped[int] = mapped_column(
    Integer,
    nullable=False
  )
  
  author_id: Mapped[int] = mapped_column(
    ForeignKey("authors.id"),
    nullable=False
  )

  author: Mapped["Author"] = relationship(
    "Author",
    back_populates="books"
  )

  reading_states: Mapped[List["ReadingState"]] = relationship(
    "ReadingState",
    back_populates="book",
    cascade="all, delete-orphan"
  )