from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Awaitable


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


class QueueResultStatus(Enum):
    SUCCESS = 0
    ERROR = 1


@dataclass
class QueueResult:
    response: Any
    status: QueueResultStatus


class QueueService(ABC):
    @abstractmethod
    async def push(self, task: type[BaseTask], data: dict[str, Any]) -> str:
        ...

    @abstractmethod
    async def is_ready(self, task_id: str) -> bool:
        ...

    @abstractmethod
    async def get_result(self, task_id: str) -> QueueResult:
        ...

    @abstractmethod
    async def wait_result(
        self, task_id: str, check_interval: float | None = None, timeout: float | None = None
    ) -> QueueResult: ...
