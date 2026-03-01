from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any



@dataclass
class BaseTask(ABC):
    @classmethod
    def get_name(cls) -> str:
        name = getattr(cls, "__task_name__", None)
        if name is None:
            raise

        return name

    @staticmethod
    @abstractmethod
    async def run(*args: Any, **kwargs: Any) -> None: ...
