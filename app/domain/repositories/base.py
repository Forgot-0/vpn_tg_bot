from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from dataclasses import dataclass

from app.domain.filters.base import BaseFilter


T = TypeVar('T')


@dataclass(frozen=True)
class PageResult(Generic[T]):
    items: tuple[T, ...]
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @property
    def next_page(self) -> int | None:
        return self.page + 1 if self.has_next else None

    @property
    def previous_page(self) -> int | None:
        return self.page - 1 if self.has_previous else None


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def find_by_filter(self, filters: BaseFilter) -> PageResult[T]:
        ...

    @abstractmethod
    async def count_by_filter(self, filters: BaseFilter) -> int:
        ...