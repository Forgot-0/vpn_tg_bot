from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.entities.base import AggregateRoot


T = TypeVar('T', bound='BaseDTO')

@dataclass
class BaseDTO(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> T: ...

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: AggregateRoot) -> T: ...