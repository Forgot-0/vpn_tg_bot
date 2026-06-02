from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.subscription_draft import SubscriptionDraft
from app.domain.repositories.subscription_drafts import SubscriptionDraftRepository
from app.infrastructure.db.mappers.subscription_drafts import SubscriptionDraftMapper
from app.infrastructure.db.models.subscription_drafts import SubscriptionDraftModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemySubscriptionDraftRepository(SQLAlchemyRepository, SubscriptionDraftRepository):
    async def get_by_id(self, draft_id: UUID) -> SubscriptionDraft | None:
        model = await self.session.get(SubscriptionDraftModel, draft_id)
        return SubscriptionDraftMapper.to_entity(model) if model else None

    async def add(self, draft: SubscriptionDraft) -> None:
        self.session.add(SubscriptionDraftMapper.to_model(draft))

    async def update(self, draft: SubscriptionDraft) -> None:
        model = await self.session.get(SubscriptionDraftModel, draft.id)
        if model is None:
            raise LookupError(f"SubscriptionDraft {draft.id} not found")
        SubscriptionDraftMapper.update_model(model, draft)

    async def list_by_user(self, user_id: UUID) -> list[SubscriptionDraft]:
        stmt = select(SubscriptionDraftModel).where(SubscriptionDraftModel.user_id == user_id)
        result = await self.session.execute(stmt)
        return [SubscriptionDraftMapper.to_entity(model) for model in result.scalars().all()]

    async def list_ready_for_checkout(self) -> list[SubscriptionDraft]:
        stmt = select(SubscriptionDraftModel).where(SubscriptionDraftModel.status == "ready_for_checkout")
        result = await self.session.execute(stmt)
        return [SubscriptionDraftMapper.to_entity(model) for model in result.scalars().all()]
