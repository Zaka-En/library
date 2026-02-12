from app.database import Base
from sqlalchemy import String, CheckConstraint
import enum
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
import bcrypt

class User(Base):

  __tablename__ = "users"

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

  def verify_password(self, plain_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = self.hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_bytes)
    
  @staticmethod
  def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


