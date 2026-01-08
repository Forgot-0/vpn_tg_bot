from dataclasses import dataclass
from uuid import uuid4

from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.entities.subscription import Subscription
from app.domain.services.subscription import SubscriptionPricingService
from app.domain.values.servers import ProtocolType, Region
from app.domain.values.users import UserId


@dataclass(frozen=True)
class GetPriceSubscriptionQuery(BaseQuery):
    duration: int
    device_count: int
    protocol_types: list[str]


@dataclass(frozen=True)
class GetPriceSubscriptionQueryHandler(BaseQueryHandler[GetPriceSubscriptionQuery, int]):
    subs_price_service: SubscriptionPricingService

    async def handle(self, query: GetPriceSubscriptionQuery) -> float:
        protocol_types=[ProtocolType(t) for t in query.protocol_types]
        subs = Subscription(
            user_id=UserId(uuid4()),
            duration=query.duration,
            device_count=query.device_count,
            protocol_types=protocol_types,
            server_id=uuid4(),
            region=Region("🇳🇱", "Нидерланды", "NL")
        )
        return await self.subs_price_service.calculate(subs)
