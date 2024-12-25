from abc import ABC, abstractmethod
from dataclasses import dataclass

from application.queries.base import BaseQuery


@dataclass
class BaseCacheService(ABC):
    @abstractmethod
    async def get(self, query: BaseQuery) -> dict: ...

    @abstractmethod
    async def set(self, key, data: dict) -> None: ...

    @abstractmethod
    def key_builder(self, *args, **kwargs) -> str: ...