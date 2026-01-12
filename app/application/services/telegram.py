from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.application.dtos.users.web_app import WebAppInitData



@dataclass
class TelegramWebAppAuth(ABC):
    @abstractmethod
    def safe_parse_webapp_init_data(self, init_data: str) -> WebAppInitData:
        ...
