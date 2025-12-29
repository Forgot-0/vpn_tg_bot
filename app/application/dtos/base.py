from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


from app.domain.entities.base import AggregateRoot


T = TypeVar('T', bound='BaseDTO')

@dataclass
class BaseDTO(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> T: ...

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: AggregateRoot) -> T: ...


TDTO = TypeVar('TDTO')


@dataclass(frozen=True)
class PaginatedResponseDTO(Generic[TDTO]):
    items: list[TDTO]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    next_page: int | None
    previous_page: int | None

