from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.infrastructure.tasks.model import BaseTask



class QueueResultStatus(Enum):
    SUCCESS = 0
    ERROR = 1


@dataclass
class QueueResult:
    response: Any
    status: QueueResultStatus


class QueueServiceInterface(ABC):
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
