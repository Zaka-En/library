from app.services.book_service import BookService
from app.models.book import Book
import pytest
from unittest.mock import AsyncMock, MagicMock

def make_mock_session(return_value):
  mock_result = MagicMock()
  mock_result.scalar_one_or_none.return_value = return_value
  mock_result.scalar_one_or_none.all.return_value = return_value

  mock_session = AsyncMock()  
  mock_session.execute.return_value = mock_result
  return mock_session


@pytest.mark.asyncio
async def test_get_by_id_returns_book():
  fake_book = Book(id=1,title="BlaBla",pages=3,author_id=1,publication_year=2023,isbn='1234567891234')
  session = make_mock_session(return_value=fake_book)

  fake_book_service = BookService(asy=session)
  result = await fake_book_service.get_by_id(book_id=1)

  assert result.title == "BlaBla"
