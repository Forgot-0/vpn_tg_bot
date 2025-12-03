from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
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



class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class SortParam:
    field: str
    order: SortOrder = SortOrder.ASC


@dataclass
class FilterParam:
    field: str
    value: int | str | list


@dataclass
class ListParams:
    sort: list[SortParam] | None = field(default=None)
    filters: list[FilterParam] | None = field(default=None)
    page: int = field(default=1)
    page_size: int = field(default=10)


@dataclass
class ListParamsWithoutPagination:
    sort: list[SortParam] | None = field(default=None)
    filters: list[FilterParam] | None = field(default=None)


@dataclass
class Pagination:
    total: int
    page: int
    page_size: int


T = TypeVar("T")

@dataclass
class PaginatedResult(Generic[T]):
    items: list[T]
    pagination: Pagination
