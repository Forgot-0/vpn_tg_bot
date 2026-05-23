from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import delete, select

from app.domain.entities.subscription import Subscription, SubscriptionPlan
from app.domain.repositories.subscriptions import SubscriptionPlanRepository, SubscriptionRepository
from app.domain.values.subscriptions import SubscriptionStatus
from app.infrastructure.db.mappers.subscriptions import SubscriptionMapper, SubscriptionPlanMapper
from app.infrastructure.db.models.subscriptions import SubscriptionModel, SubscriptionPlanModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository

class SQLAlchemySubscriptionRepository(
    SQLAlchemyRepository,
    SubscriptionRepository,
):
    async def get_by_id(self, subscription_id: UUID) -> Subscription | None:
        query = select(SubscriptionModel).where(
            SubscriptionModel.id == subscription_id
        )
        subscription = (await self.session.execute(query)).scalar()
        return SubscriptionMapper.to_domain(subscription) if subscription else None

    async def add(self, entity: Subscription) -> None:
        self.session.add(SubscriptionMapper.to_model(entity))

    async def update(self, subscription_entity: Subscription) -> None:
        query = select(SubscriptionModel).where(
            SubscriptionModel.id == subscription_entity.id
        )
        subscription = (await self.session.execute(query)).scalar()
        if subscription is None:
            raise ValueError(f"Subscription {subscription_entity.id} not found")
        SubscriptionMapper.update_model(subscription, subscription_entity)

    async def delete(self, subscription_id: str) -> None:
        await self.session.execute(
            delete(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        )

    async def list_by_user(self, user_id: UUID) -> list[Subscription]:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return [SubscriptionMapper.to_domain(m) for m in result.scalars().all()]

    async def list_by_status(self, status: SubscriptionStatus) -> list[Subscription]:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.status == status.value
        )
        result = await self.session.execute(stmt)
        return [SubscriptionMapper.to_domain(m) for m in result.scalars().all()]

    async def list_expiring(self, within_days: int) -> list[Subscription]:
        today = date.today()
        boundary = today + timedelta(days=within_days)
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.status == SubscriptionStatus.ACTIVE.value,
            SubscriptionModel.expires_at.isnot(None),
            SubscriptionModel.expires_at <= boundary,
            SubscriptionModel.expires_at >= today,
        )
        result = await self.session.execute(stmt)
        return [SubscriptionMapper.to_domain(m) for m in result.scalars().all()]


class SQLAlchemySubscriptionPlanRepository(
    SQLAlchemyRepository,
    SubscriptionPlanRepository,
):
    async def get(self, subscription_plan_id: UUID) -> SubscriptionPlan | None:
        query = select(SubscriptionPlanModel).where(
            SubscriptionPlanModel.id == subscription_plan_id
        )
        subscription_plan = (await self.session.execute(query)).scalar()
        return SubscriptionPlanMapper.to_domain(subscription_plan) if subscription_plan else None

    async def add(self, subscription_plan_entity: SubscriptionPlan) -> None:
        self.session.add(SubscriptionPlanMapper.to_model(subscription_plan_entity))

    async def update(self, subscription_plan_entity: SubscriptionPlan) -> None:
        query = select(SubscriptionPlanModel).where(
            SubscriptionPlanModel.id == subscription_plan_entity.id
        )
        subscription = (await self.session.execute(query)).scalar()
        if subscription is None:
            raise ValueError(f"Subscription {subscription_plan_entity.id} not found")
        SubscriptionPlanMapper.update_model(subscription, subscription_plan_entity)

    async def delete(self, subscription_plan_id: UUID) -> None:
        await self.session.execute(
            delete(SubscriptionPlanModel).where(SubscriptionPlanModel.id == subscription_plan_id)
        )

    async def get_by_code(self, code: str) -> SubscriptionPlan | None:
        stmt = select(SubscriptionPlanModel).where(
            SubscriptionPlanModel.code == code
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return SubscriptionPlanMapper.to_domain(model) if model else None

    async def list_active(self) -> list[SubscriptionPlan]:
        stmt = select(SubscriptionPlanModel).where(
            SubscriptionPlanModel.is_active.is_(True)
        )
        result = await self.session.execute(stmt)
        return [SubscriptionPlanMapper.to_domain(m) for m in result.scalars().all()]
