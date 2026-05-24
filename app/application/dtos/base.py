from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Self, TypeVar


from app.domain.entities.base import AggregateRoot



@dataclass
class BaseDTO(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: AggregateRoot) -> Self: ...


TDTO = TypeVar('TDTO', bound=BaseDTO)


@dataclass(frozen=True)
class PaginatedResponseDTO(Generic[TDTO]):
    items: list[TDTO]
    total: int
    page: int
    page_size: int
