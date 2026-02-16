# app/services/author_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.author import Author
import asyncio
from broadcaster import Broadcast 
from app.schema.inputs import UpdateAuthorInput, CreateAuthorInput
from strawberry import UNSET
from typing import AsyncGenerator, Sequence, List, Optional
from dataclasses import dataclass
import base64

@dataclass
class PaginatedAuthors:
  items: List[Author]
  has_next_page: bool
  start_cursor: Optional[str]
  end_cursor: Optional[str]

class AuthorService:
  def __init__(self, session: AsyncSession, broadcast: Broadcast):
    self.session = session
    self.broadcast = broadcast 

  async def get_all(self) -> Sequence[Author]:
    result = await self.session.execute(select(Author))
    return result.scalars().all()

  async def get_by_id(self, author_id: int) -> Author:
    result = await self.session.execute(select(Author).filter(Author.id == author_id))
    return result.scalar_one_or_none()

  async def create(self, data: CreateAuthorInput) -> Author:
    author = Author(
        name=data.name,
        biography=data.biography,
        fullname=data.fullname,
        country=data.country
    )
    self.session.add(author)
    await self.session.commit()
    await self.session.refresh(author)
    return author

  async def update(self, data_input: UpdateAuthorInput) -> Author:
    
    author_id = data_input.id

    await self.broadcast.publish(channel="NOTIFICATIONS", message="Incializando actualizacion")
    await asyncio.sleep(2) #simulate a delay
    
    author = await self.get_by_id(author_id)
    if not author:
      raise ValueError(f"Author with id {author_id} not found")

    input_dict = vars(data_input)
    for key, value in input_dict.items():
      if key != 'id' and value not in [None, UNSET] :
        setattr(author, key, value)

    await self.session.commit()
    await self.session.refresh(author)
    
    await self.broadcast.publish(channel="NOTIFICATIONS", message="¡Autor actualizado con éxito!")
    return author
  
  async def authors_genrator(self, limite: int, after_id: int = 0) ->AsyncGenerator[Author,None]:
    query = select(Author).order_by(Author.id)

    if after_id:
      query = query.filter(Author.id > after_id)

    query = query.limit(limite + 1)
  
    result = await self.session.execute(query)

    for author in result.scalars():
      yield author

  def _encode_cursor(self, author_id: int) -> str:
    return base64.b64encode(f"arrayconnection:{author_id}".encode()).decode()
  
  def _decode_cursor(self, cursor: str) -> int:
    try:
      return int(base64.b64decode(cursor).decode().split(':')[-1])
    except Exception:
      return 0 
    
  async def get_paginated(self, limit: int, after_cursor: Optional[str] = None) -> PaginatedAuthors:
    after_id = self._decode_cursor(after_cursor) if after_cursor else 0
    
    query = select(Author).where(Author.id > after_id).order_by(Author.id).limit(limit + 1)
    result = await self.session.execute(query)
    authors = list(result.scalars().all())

    has_next_page = len(authors) > limit
    items = authors[:limit] if has_next_page else authors

    start_cursor = self._encode_cursor(items[0].id) if items else None
    end_cursor = self._encode_cursor(items[-1].id) if items else None

    return PaginatedAuthors(
      items=items,
      has_next_page=has_next_page,
      start_cursor=start_cursor,
      end_cursor=end_cursor
    )