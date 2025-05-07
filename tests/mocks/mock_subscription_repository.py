from typing import List, Optional
from uuid import UUID
from domain.entities.subscription import Subscription
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.values.subscriptions import SubscriptionId


class MockSubscriptionRepository(BaseSubscriptionRepository):
    def __init__(self) -> None:
        self._data: dict[SubscriptionId, Subscription] = {}

    async def create(self, subscription: Subscription) -> None:
        self._data[subscription.id] = subscription

    async def deactivate(self, id: SubscriptionId) -> None:
        if id in self._data:
            sub = self._data[id]
            self._data[id] = sub

    async def activate(self, id: SubscriptionId) -> None:
        if id in self._data:
            sub = self._data[id]
            self._data[id] = sub

    async def get(self) -> List[Subscription]:
        return [sub for sub in self._data.values()]

    async def get_by_id(self, id: SubscriptionId) -> Optional[Subscription]:
        return self._data.get(id)