# app/services/author_service.py
import asyncio
import base64
from dataclasses import dataclass
from typing import AsyncGenerator, List, Optional

from broadcaster import Broadcast
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from strawberry import UNSET

from app.models.author import Author
from app.schema.inputs import CreateAuthorInput, UpdateAuthorInput

from .base import BaseService, SingletonService


@dataclass
class PaginatedAuthors:
    items: List[Author]
    has_next_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]


class AuthorService(SingletonService, BaseService[Author]):
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession], broadcast: Broadcast
    ):
        if not hasattr(self, "session_factory"):
            self.session_factory = session_factory
            self.broadcast = broadcast

    async def get_all(self) -> List[Author]:
        async with self.session_factory() as session:
            result = await session.execute(select(Author))
            return list(result.scalars().all())

    async def get_by_id(self, author_id: int) -> Optional[Author]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(Author).filter(Author.id == author_id)
            )
            return result.scalar_one_or_none()

    async def get_by_ids(self, authors_ids: list[int]) -> List[Author]:
        async with self.session_factory() as session:
            return list(
                (
                    await session.execute(
                        select(Author).where(Author.id.in_(authors_ids))
                    )
                )
                .scalars()
                .all()
            )

    async def create(self, data: CreateAuthorInput) -> Author:
        async with self.session_factory() as session:
            author = Author(
                name=data.name,
                biography=data.biography,
                fullname=data.fullname,
                country=data.country,
            )
            session.add(author)
            await session.commit()
            await session.refresh(author)
            return author

    async def update(self, data_input: UpdateAuthorInput) -> Author:
        author_id = data_input.id
        await self.broadcast.publish(
            channel="NOTIFICATIONS", message="Incializando actualizacion"
        )
        await asyncio.sleep(2)
        async with self.session_factory() as session:
            result = await session.execute(
                select(Author).filter(Author.id == author_id)
            )
            author = result.scalar_one_or_none()
            if not author:
                raise ValueError(f"Author with id {author_id} not found")
            input_dict = vars(data_input)
            for key, value in input_dict.items():
                if key != "id" and value not in [None, UNSET]:
                    setattr(author, key, value)
            await session.commit()
            await session.refresh(author)
        await self.broadcast.publish(
            channel="NOTIFICATIONS", message="¡Autor actualizado con éxito!"
        )
        return author

    async def authors_genrator(
        self, limite: int, after_id: int = 0
    ) -> AsyncGenerator[Author, None]:
        async with self.session_factory() as session:
            query = select(Author).order_by(Author.id)
            if after_id:
                query = query.filter(Author.id > after_id)
            query = query.limit(limite + 1)
            result = await session.execute(query)
            for author in result.scalars():
                yield author

    def _encode_cursor(self, author_id: int) -> str:
        return base64.b64encode(f"arrayconnection:{author_id}".encode()).decode()

    def _decode_cursor(self, cursor: str) -> int:
        try:
            return int(base64.b64decode(cursor).decode().split(":")[-1])
        except Exception:
            return 0

    async def get_paginated(
        self, limit: int, after_cursor: Optional[str] = None
    ) -> PaginatedAuthors:
        after_id = self._decode_cursor(after_cursor) if after_cursor else 0
        async with self.session_factory() as session:
            query = (
                select(Author)
                .where(Author.id > after_id)
                .order_by(Author.id)
                .limit(limit + 1)
            )
            result = await session.execute(query)
            authors = list(result.scalars().all())
        has_next_page = len(authors) > limit
        items = authors[:limit] if has_next_page else authors
        start_cursor = self._encode_cursor(items[0].id) if items else None
        end_cursor = self._encode_cursor(items[-1].id) if items else None
        return PaginatedAuthors(
            items=items,
            has_next_page=has_next_page,
            start_cursor=start_cursor,
            end_cursor=end_cursor,
        )

    async def delete(self, author_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                select(Author).filter(Author.id == author_id)
            )
            author = result.scalar_one_or_none()
            if not author:
                return False
            await session.delete(author)
            await session.commit()
            return True
