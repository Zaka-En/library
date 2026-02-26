import strawberry
from typing import Optional

@strawberry.input
class CreateAuthorInput:
  name: str
  biography: Optional[str] = None
  fullname: Optional[str] = None
  country: str



@strawberry.input
class UpdateAuthorInput:
  id:int 
  name:  Optional[str] = strawberry.UNSET
  biography: Optional[str] =  strawberry.UNSET
  fullname: Optional[str] =  strawberry.UNSET
  country: Optional[str] =  strawberry.UNSET

@strawberry.input
class CreateBookInput:
  title: str 
  isbn: str
  publication_year: int
  pages: int
  author_id: int

@strawberry.input
class UpdateBookInput:
  id:int
  title: Optional[str] = strawberry.UNSET
  isbn: Optional[str] = strawberry.UNSET
  publication_year: Optional[int] = strawberry.UNSET
  pages: Optional[int] = strawberry.UNSET
  author_id: Optional[int] = strawberry.UNSET


@strawberry.input
class StartReadingInput:
  book_id: int
  user_id: int


@strawberry.input
class UpdateProgressInput:
  id: int  # ID del ReadingState
  current_page: int


@strawberry.input
class FinishReadingInput:
  id: int  # ID del ReadingState

@strawberry.input
class RegisterInput:
  name: str
  email: str
  password: str
  fullname: Optional[str] = None
  rol: str = "user"

@strawberry.input
class LoginInput:
  email: str
  password: str


@strawberry.input
class UpdateUserInput:
  id: int 
  name: Optional[str] = None
  username: Optional[str] = None
  email: Optional[str] = None
  fullname: Optional[str] = None
  second_name: Optional[str] = None
  street_adress: Optional[str] = None
  city: Optional[str] = None
  province: Optional[str] = None
  zip_code: Optional[str] = None
  about: Optional[str] = None




import strawberry
from datetime import date as pyDate

@strawberry.input
class RoomBookingInput:
  room_id: int
  user_id: int
  date: str  # Formato YYYY-MM-DD iso 8601
  attendees_count: int
  hour:int

  def to_model_dict(self) -> dict:
    data = strawberry.asdict(self)
    data['date'] = pyDate.fromisoformat(self.date)
    return data