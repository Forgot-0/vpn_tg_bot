from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.subscription import Subscription
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.values.subscriptions import SubscriptionStatus
from app.infrastructure.db.mappers.subscriptions import SubscriptionMapper
from app.infrastructure.db.models.subscriptions import SubscriptionModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemySubscriptionRepository(SQLAlchemyRepository, SubscriptionRepository):
    async def get_by_id(self, subscription_id: UUID) -> Subscription | None:
        model = await self.session.get(SubscriptionModel, subscription_id)
        return SubscriptionMapper.to_entity(model) if model else None

    async def add(self, subscription: Subscription) -> None:
        self.session.add(SubscriptionMapper.to_model(subscription))

    async def update(self, subscription: Subscription) -> None:
        model = await self.session.get(SubscriptionModel, subscription.id)
        if model is None:
            raise LookupError(f"Subscription {subscription.id} not found")
        SubscriptionMapper.update_model(model, subscription)

    async def list_by_user(self, user_id: UUID) -> list[Subscription]:
        stmt = select(SubscriptionModel).where(SubscriptionModel.user_id == user_id)
        result = await self.session.execute(stmt)
        return [SubscriptionMapper.to_entity(model) for model in result.scalars().all()]

    async def list_by_status(self, status: SubscriptionStatus) -> list[Subscription]:
        stmt = select(SubscriptionModel).where(SubscriptionModel.status == status.value)
        result = await self.session.execute(stmt)
        return [SubscriptionMapper.to_entity(model) for model in result.scalars().all()]

    async def list_expiring_within(self, days: int) -> list[Subscription]:
        today = date.today()
        deadline = today + timedelta(days=days)
        stmt = (
            select(SubscriptionModel)
            .where(SubscriptionModel.expires_at.is_not(None))
            .where(SubscriptionModel.expires_at >= today)
            .where(SubscriptionModel.expires_at <= deadline)
            .where(
                SubscriptionModel.status.in_(
                    [
                        SubscriptionStatus.ACTIVE.value,
                        SubscriptionStatus.SUSPENDED.value,
                    ]
                )
            )
        )
        result = await self.session.execute(stmt)
        return [SubscriptionMapper.to_entity(model) for model in result.scalars().all()]

    async def list_traffic_exceeded(self) -> list[Subscription]:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.status.in_(
                [SubscriptionStatus.ACTIVE.value, SubscriptionStatus.SUSPENDED.value]
            )
        )
        result = await self.session.execute(stmt)
        exceeded: list[Subscription] = []
        for model in result.scalars().all():
            entity = SubscriptionMapper.to_entity(model)
            if entity.is_traffic_exceeded:
                exceeded.append(entity)
        return exceeded

    async def get_by_payment_order(self, payment_order_id: UUID) -> Subscription | None:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.payment_order_id == payment_order_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return SubscriptionMapper.to_entity(model) if model else None
