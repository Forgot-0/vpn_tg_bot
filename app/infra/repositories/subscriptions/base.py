from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.entities.subscription import Subscription


@dataclass
class BaseSubscriptionRepository(ABC):

    @abstractmethod
    async def create(self, subscription: Subscription) -> None:
        ...

    @abstractmethod
    async def pay(self, id: UUID, payment_id: str) -> None:
        ...

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> Subscription | None:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Subscription | None:
        ...

    @abstractmethod
    async def delete_not_paid_sub(self, tg_id: int) -> None:
        ...

    @abstractmethod
    async def get_active_subscription(self, tg_id: int) -> list[Subscription] | None:
        ...

    @abstractmethod
    async def set_vpn_url(self, subs_id: UUID, vpn_url: str) -> None:
        ...