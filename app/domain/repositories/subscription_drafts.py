from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.subscription_draft import SubscriptionDraft


class SubscriptionDraftRepository(ABC):
    @abstractmethod
    async def get_by_id(self, draft_id: UUID) -> SubscriptionDraft | None: ...

    @abstractmethod
    async def add(self, draft: SubscriptionDraft) -> None: ...

    @abstractmethod
    async def update(self, draft: SubscriptionDraft) -> None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[SubscriptionDraft]: ...

    @abstractmethod
    async def list_ready_for_checkout(self) -> list[SubscriptionDraft]: ...
