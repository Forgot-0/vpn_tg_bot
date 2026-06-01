from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


class BaseTemplate(ABC):
    _env: Environment | None = None

    @property
    def env(self) -> Environment:
        if self._env is None:
            self._env = Environment(
                loader=FileSystemLoader(self._get_dir()), autoescape=True
            )
        return self._env

    @abstractmethod
    def _get_dir(self) -> Path: ...

    @abstractmethod
    def _get_name(self) -> str: ...

    def _get_data(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith("_") and not k.startswith("__")}

    def render(self) -> str:
        return self.env.get_template(self._get_name()).render(self._get_data())


@dataclass
class EmailData:
    subject: str
    recipient: str
    sender_address: str | None = None
    sender_name: str | None = None


class BaseMailService(ABC):
    @abstractmethod
    async def send(self, template: BaseTemplate, email_data: EmailData) -> None:
        ...

    @abstractmethod
    async def queue(self, template: BaseTemplate, email_data: EmailData) -> str:
        ...

    @abstractmethod
    async def send_plain(self, subject: str, recipient: str, body: str) -> None:
        ...

    @abstractmethod
    async def queue_plain(self, subject: str, recipient: str, body: str) -> str:
        ...
