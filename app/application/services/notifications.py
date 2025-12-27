from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.user import User
from app.domain.values.servers import VPNConfig


@dataclass
class NotificationSevice(ABC):

    @abstractmethod
    async def send_subscription_config(self, user: User, vpn_config: VPNConfig) -> None:
        ...
