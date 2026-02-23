from app.database import Base
from sqlalchemy import String, CheckConstraint, Text
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
import bcrypt

if TYPE_CHECKING:
  from .reading_state import ReadingState
  from .room_bookings import RoomBooking

class User(Base):

  __tablename__ = "users"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True
  )

  email: Mapped[str] = mapped_column(
    String(254),
    nullable=False,
    unique=True
  )

  name: Mapped[str] = mapped_column(
    String(50),
    nullable=False
  )

  username: Mapped[str] = mapped_column(
    String(50),
    nullable=False
  )

  second_name: Mapped[Optional[str]] = mapped_column(
    String(50),
    nullable=True
  )

  street_adress: Mapped[Optional[str]] = mapped_column(
    String(255),
    nullable=True
  ) 

  city: Mapped[Optional[str]] = mapped_column(
    String(50),
    nullable=True
  )

  province: Mapped[Optional[str]] = mapped_column(
    String(50),
    nullable=True
  )

  zip_code : Mapped[Optional[str]] = mapped_column(
    String(5),
    nullable=True
  )

  about: Mapped[Optional[str]] = mapped_column(
    Text,
    nullable=True
  )

  fullname: Mapped[Optional[str]] = mapped_column(
    String(100),
    nullable=True
  )

  password: Mapped[str] = mapped_column(String(255), nullable=False)

  rol: Mapped[str] = mapped_column(
    String(20), 
    server_default="user", 
    nullable=False
  )


  __table_args__ = (
    CheckConstraint(rol.in_(["user", "admin"]), name="check_user_role"),
  )

  reading_states: Mapped[List["ReadingState"]] = relationship(
    "ReadingState",
    back_populates="user",
    cascade="all, delete-orphan"
  )

  room_bookings: Mapped[List["RoomBooking"]] =relationship(
    back_populates="user",
  )

  def verify_password(self, plain_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = self.password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_bytes)
    
  @staticmethod
  def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


