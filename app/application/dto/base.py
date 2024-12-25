from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseDTO(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'BaseDTO': ...