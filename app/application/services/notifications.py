from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.subscription import Subscription
from app.domain.entities.user import User
from app.domain.values.servers import VPNConfig


@dataclass
class NotificationSevice(ABC):

    @abstractmethod
    async def send_subscription_config(self, user: User, vpn_config: VPNConfig) -> None:
        ...

    @abstractmethod
    async def send_subscription_activated(self, user: User, subscription: Subscription) -> None:
        ...

    @abstractmethod
    async def send_subscription_expiring_soon(self, user: User, subscription: Subscription)-> None:
        ...

    @abstractmethod
    async def send_subscription_expired(self, user: User, subscription: Subscription) -> None:
        ...

