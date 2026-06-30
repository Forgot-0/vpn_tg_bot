from __future__ import annotations

from dataclasses import dataclass

from app.application.dtos.subscriptions import PlanDTO, PlanPriceDTO
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.plans import PlanRepository


@dataclass(frozen=True)
class GetPublicPlansQuery(BaseQuery):
    ...


@dataclass(frozen=True)
class GetPublicPlansQueryHandler(BaseQueryHandler[GetPublicPlansQuery, list[PlanDTO]]):
    plan_repository: PlanRepository

    async def handle(self, query: GetPublicPlansQuery) -> list[PlanDTO]:
        plans = await self.plan_repository.list_public()

        result: list[PlanDTO] = []
        for plan in plans:
            if not plan.is_active:
                continue

            prices = [
                PlanPriceDTO(amount=p.amount, currency=p.currency)
                for p in sorted(plan.price, key=lambda x: x.amount)
            ]

            limits = plan.limit

            result.append(
                PlanDTO(
                    id=plan.id,
                    code=plan.code,
                    name=plan.name,
                    description=plan.description,
                    prices=prices,
                    duration_days=limits.duration_days.days if limits else None,
                    traffic_gb=limits.traffic_limit_gb.gb if limits else None,
                    max_devices=limits.max_devices.max_devices if limits else None,
                    is_trial=plan.is_trial,
                    order_index=plan.order_index,
                )
            )

        return sorted(result, key=lambda p: p.order_index)
