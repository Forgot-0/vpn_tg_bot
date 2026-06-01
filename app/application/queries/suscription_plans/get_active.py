from dataclasses import dataclass

from app.application.dtos.subscriptions import SubscriptionPlanDTO
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.subscriptions import SubscriptionPlanRepository



@dataclass(frozen=True)
class GetPublicPlansQuery(BaseQuery):
    ...


@dataclass(frozen=True)
class GetPublicPlansHandler(BaseQueryHandler[GetPublicPlansQuery, list[SubscriptionPlanDTO]]):
    plan_repository: SubscriptionPlanRepository

    async def handle(self, query: GetPublicPlansQuery) -> list[SubscriptionPlanDTO]:
        plans = await self.plan_repository.list_public_active()
        return [SubscriptionPlanDTO.from_entity(plan) for plan in plans]
