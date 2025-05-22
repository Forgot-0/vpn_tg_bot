from dataclasses import dataclass
import logging
from uuid import UUID

from application.dtos.subsciprions.subscription import SubscriptionDTO
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.values.subscriptions import SubscriptionId


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetByIdQuery(BaseQuery):
    subscription_id: UUID


@dataclass(frozen=True)
class GetByIdQueryHandler(BaseQueryHandler[GetByIdQuery, SubscriptionDTO]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, query: GetByIdQuery) -> SubscriptionDTO:
        subscription = await self.subscription_repository.get_by_id(SubscriptionId(query.subscription_id))

        if not subscription:
            raise


        subscription_dto = SubscriptionDTO.from_entity(subscription)

        logger.debug(
            "Get subscription by id",
            extra={"subscription_id": query.subscription_id, "subscription": subscription_dto}
        )
        return subscription_dto