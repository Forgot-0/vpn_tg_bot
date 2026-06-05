from dataclasses import dataclass

from app.application.dtos.subscriptions import PlanDTO
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.plans import PlanRepository



@dataclass(frozen=True)
class GetPublicPlansQuery(BaseQuery):
    ...


@dataclass(frozen=True)
class GetPublicPlansHandler(BaseQueryHandler[GetPublicPlansQuery, list[PlanDTO]]):
    plan_repository: PlanRepository

    async def handle(self, query: GetPublicPlansQuery) -> list[PlanDTO]:
        plans = await self.plan_repository.list_public_active()
        return [PlanDTO.from_entity(plan) for plan in plans]
