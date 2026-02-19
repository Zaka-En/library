from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Generic, List, Any

T = TypeVar("T")

class BaseService(ABC, Generic[T]):

  @abstractmethod
  async def get_by_id(self, id: int) -> Optional[T]:
    ...

  @abstractmethod
  async def get_all(self) -> List[T]:
    ...

  @abstractmethod
  async def get_by_ids(self, ids: List[int]) -> List[T]:
    ...
  
  @abstractmethod
  async def create(self, data: Any) -> T:
    ...

  @abstractmethod
  async def update(self, data: Any) -> T:
    ...

  @abstractmethod
  async def delete(self, id: int) -> T:
    ...

class SingletonServiceInstance:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance