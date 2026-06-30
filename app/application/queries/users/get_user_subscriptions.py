from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.subscriptions import SubscriptionDTO
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.plans import PlanRepository
from app.domain.repositories.subscriptions import SubscriptionRepository


@dataclass(frozen=True)
class GetUserSubscriptionsQuery(BaseQuery):
    user_id: UUID


@dataclass(frozen=True)
class GetUserSubscriptionsQueryHandler(BaseQueryHandler[GetUserSubscriptionsQuery, list[SubscriptionDTO]]):
    subscription_repository: SubscriptionRepository
    plan_repository: PlanRepository

    async def handle(self, query: GetUserSubscriptionsQuery) -> list[SubscriptionDTO]:
        subscriptions = await self.subscription_repository.list_by_user(query.user_id)

        result: list[SubscriptionDTO] = []
        for sub in subscriptions:
            plan = await self.plan_repository.get_by_id(sub.plan_id)
            plan_name = plan.name if plan else "Unknown"

            limits = sub.limit

            result.append(
                SubscriptionDTO(
                    id=sub.id,
                    user_id=sub.user_id,
                    plan_id=sub.plan_id,
                    plan_name=plan_name,
                    status=sub.status,
                    activated_at=sub.activated_at,
                    expires_at=sub.expires_at,
                    bytes_used=sub.usage.bytes_used,
                    traffic_limit_bytes=limits.traffic_limit_gb.bytes_limit,
                    duration_days=limits.duration_days.days,
                    max_devices=limits.max_devices.max_devices,
                )
            )

        return result
