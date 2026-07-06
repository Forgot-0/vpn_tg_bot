from uuid import UUID

from sqlalchemy import select

from app.domain.entities.plan import SubscriptionPlan
from app.domain.repositories.plans import PlanRepository
from app.domain.values.subscriptions import PlanVisibility
from app.infrastructure.db.mappers.plan import PlanMapper
from app.infrastructure.db.models.plan import SubscriptionPlanModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLPlanRepository(SQLAlchemyRepository, PlanRepository):
    async def get_by_id(self, plan_id: UUID) -> SubscriptionPlan | None:
        result = await self.session.execute(select(SubscriptionPlanModel).where(SubscriptionPlanModel.id == plan_id))
        plan_model = result.scalar()
        return PlanMapper.from_plan_model_to_domain(plan_model) if plan_model is not None else None

    async def get_by_code(self, code: str) -> SubscriptionPlan | None:
        result = await self.session.execute(select(SubscriptionPlanModel).where(SubscriptionPlanModel.code == code))
        plan_model = result.scalar()
        return PlanMapper.from_plan_model_to_domain(plan_model) if plan_model is not None else None

    async def list_public(self) -> list[SubscriptionPlan]:
        result = await self.session.execute(
            select(SubscriptionPlanModel).where(SubscriptionPlanModel.visibility == PlanVisibility.PUBLIC)
        )
        return [PlanMapper.from_plan_model_to_domain(model) for model in result.scalars()]

    async def list_all(self) -> list[SubscriptionPlan]:
        result = await self.session.execute(select(SubscriptionPlanModel))
        return [PlanMapper.from_plan_model_to_domain(model) for model in result.scalars()]

    async def add(self, plan: SubscriptionPlan) -> None:
        self.session.add(PlanMapper.from_plan_domain_to_model(plan))

    async def update(self, plan: SubscriptionPlan) -> None:
        await self.session.merge(PlanMapper.from_plan_domain_to_model(plan))
