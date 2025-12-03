from typing import List, Optional
from uuid import UUID
from app.domain.entities.subscription import Subscription
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId


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

    async def get_by_user(self, user_id: UserId) -> List[Subscription]:
        res = []
        for subs in self._data.values():
            if subs.user_id == user_id:
                res.append(subs)
        return res

    async def update(self, subscription: Subscription) -> None:
        self._data[subscription.id] = subscription