from datetime import timedelta
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.subscription import Subscription
from app.domain.repositories.subscriptions import SubscriptionRepository
from app.domain.services.clock import now_utc
from app.domain.values.subscriptions import SubscriptionStatus
from app.infrastructure.db.mappers.subscription import SubscriptionMapper
from app.infrastructure.db.models.subscription import SubscriptionModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLSubscriptionRepository(SQLAlchemyRepository, SubscriptionRepository):
    async def get_by_id(self, subscription_id: UUID) -> Subscription | None:
        result = await self.session.execute(select(SubscriptionModel).where(SubscriptionModel.id == subscription_id))
        subscription_model = result.scalar()
        return SubscriptionMapper.from_subscription_model_to_domain(subscription_model) if subscription_model is not None else None

    async def list_by_user(self, user_id: UUID) -> list[Subscription]:
        result = await self.session.execute(select(SubscriptionModel).where(SubscriptionModel.user_id == user_id))
        return [SubscriptionMapper.from_subscription_model_to_domain(model) for model in result.scalars()]

    async def list_by_status(self, status: SubscriptionStatus) -> list[Subscription]:
        result = await self.session.execute(select(SubscriptionModel).where(SubscriptionModel.status == status.value))
        return [SubscriptionMapper.from_subscription_model_to_domain(model) for model in result.scalars()]

    async def list_expiring_before(self, *, cutoff_days: int) -> list[Subscription]:
        cutoff = now_utc() + timedelta(days=cutoff_days)
        result = await self.session.execute(
            select(SubscriptionModel).where(
                SubscriptionModel.expires_at.is_not(None),
                SubscriptionModel.expires_at <= cutoff,
            )
        )
        return [SubscriptionMapper.from_subscription_model_to_domain(model) for model in result.scalars()]

    async def add(self, subscription: Subscription) -> None:
        self.session.add(SubscriptionMapper.from_subscription_domain_to_model(subscription))

    async def update(self, subscription: Subscription) -> None:
        await self.session.merge(SubscriptionMapper.from_subscription_domain_to_model(subscription))
