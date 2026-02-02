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
  name:  Optional[str]
  biography: Optional[str]
  fullname: Optional[str]
  country: Optional[str]

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
  title: Optional[str]
  isbn: Optional[str]
  publication_year: Optional[int]
  pages: Optional[int]
  author_id: Optional[int]


@strawberry.input
class StartReadingInput:
  book_id: int
  user_id: str


@strawberry.input
class UpdateProgressInput:
  id: int  # ID del ReadingState
  current_page: int


@strawberry.input
class FinishReadingInput:
  id: int  # ID del ReadingState