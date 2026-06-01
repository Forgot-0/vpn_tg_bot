from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.subscription_plan import SubscriptionPlan
from app.domain.repositories.subscriptions import SubscriptionPlanRepository
from app.infrastructure.db.mappers.subscription_plans import SubscriptionPlanMapper
from app.infrastructure.db.models.subscription_plans import SubscriptionPlanModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemySubscriptionPlanRepository(SQLAlchemyRepository, SubscriptionPlanRepository):

    async def get_by_id(self, plan_id: UUID) -> SubscriptionPlan | None:
        model = await self.session.get(SubscriptionPlanModel, plan_id)
        return SubscriptionPlanMapper.to_entity(model) if model else None

    async def get_by_code(self, code: str) -> SubscriptionPlan | None:
        stmt = select(SubscriptionPlanModel).where(SubscriptionPlanModel.code == code)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return SubscriptionPlanMapper.to_entity(model) if model else None

    async def add(self, plan: SubscriptionPlan) -> None:
        self.session.add(SubscriptionPlanMapper.to_model(plan))

    async def update(self, plan: SubscriptionPlan) -> None:
        model = await self.session.get(SubscriptionPlanModel, plan.id)
        if model is None:
            raise LookupError(f"SubscriptionPlan {plan.id} not found")
        SubscriptionPlanMapper.update_model(model, plan)

    async def list_public_active(self) -> list[SubscriptionPlan]:
        stmt = (
            select(SubscriptionPlanModel)
            .where(SubscriptionPlanModel.is_active.is_(True))
            .where(SubscriptionPlanModel.is_public.is_(True))
            .order_by(SubscriptionPlanModel.sort_order.asc())
        )
        result = await self.session.execute(stmt)
        return [SubscriptionPlanMapper.to_entity(model) for model in result.scalars().all()]
