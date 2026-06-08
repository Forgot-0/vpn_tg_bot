from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.plan import Plan
from app.domain.repositories.plans import PlanRepository
from app.infrastructure.db.mappers.plans import PlanMapper
from app.infrastructure.db.models.plans import PlanModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemyPlanRepository(SQLAlchemyRepository, PlanRepository):

    async def get_by_id(self, plan_id: UUID) -> Plan | None:
        model = await self.session.get(PlanModel, plan_id)
        return PlanMapper.to_entity(model) if model else None

    async def get_by_code(self, code: str) -> Plan | None:
        stmt = select(PlanModel).where(PlanModel.code == code)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PlanMapper.to_entity(model) if model else None

    async def add(self, plan: Plan) -> None:
        self.session.add(PlanMapper.to_model(plan))

    async def update(self, plan: Plan) -> None:
        model = await self.session.get(PlanModel, plan.id)
        if model is None:
            raise LookupError(f"Plan {plan.id} not found")
        PlanMapper.update_model(model, plan)

    async def list_public_active(self) -> list[Plan]:
        stmt = (
            select(PlanModel)
            .where(PlanModel.is_active.is_(True))
            .where(PlanModel.is_public.is_(True))
            .order_by(PlanModel.sort_order.asc())
        )
        result = await self.session.execute(stmt)
        return [PlanMapper.to_entity(model) for model in result.scalars().all()]
