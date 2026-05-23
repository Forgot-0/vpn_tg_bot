from abc import ABC
from typing import Generic, TypeVar

from app.domain.entities.base import AggregateRoot


EntityT = TypeVar("EntityT", bound=AggregateRoot)
IdT = TypeVar("IdT")


class Repository(ABC, Generic[EntityT, IdT]):
    ...
