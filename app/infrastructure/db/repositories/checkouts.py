from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.checkout import CheckoutSession
from app.domain.repositories.checkouts import CheckoutSessionRepository
from app.infrastructure.db.mappers.checkouts import CheckoutSessionMapper
from app.infrastructure.db.models.checkouts import CheckoutSessionModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemyCheckoutSessionRepository(SQLAlchemyRepository, CheckoutSessionRepository):
    async def get_by_id(self, checkout_session_id: UUID) -> CheckoutSession | None:
        model = await self.session.get(CheckoutSessionModel, checkout_session_id)
        return CheckoutSessionMapper.to_entity(model) if model else None

    async def add(self, checkout: CheckoutSession) -> None:
        self.session.add(CheckoutSessionMapper.to_model(checkout))

    async def update(self, checkout: CheckoutSession) -> None:
        model = await self.session.get(CheckoutSessionModel, checkout.id)
        if model is None:
            raise LookupError(f"CheckoutSession {checkout.id} not found")
        CheckoutSessionMapper.update_model(model, checkout)

    async def list_by_user(self, user_id: UUID) -> list[CheckoutSession]:
        stmt = select(CheckoutSessionModel).where(CheckoutSessionModel.user_id == user_id)
        result = await self.session.execute(stmt)
        return [CheckoutSessionMapper.to_entity(model) for model in result.scalars().all()]

    async def list_ready_for_checkout(self) -> list[CheckoutSession]:
        stmt = select(CheckoutSessionModel).where(CheckoutSessionModel.status == "ready_for_checkout")
        result = await self.session.execute(stmt)
        return [CheckoutSessionMapper.to_entity(model) for model in result.scalars().all()]
