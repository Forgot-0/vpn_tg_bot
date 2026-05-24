from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[T]):
    value: T

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def as_generic_type(self) -> T:
        ...
