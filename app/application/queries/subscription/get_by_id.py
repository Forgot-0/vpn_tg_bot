from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetByIdQuery(BaseQuery):
    subscription_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetByIdQueryHandler(BaseQueryHandler[GetByIdQuery, SubscriptionDTO]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, query: GetByIdQuery) -> SubscriptionDTO:
        subscription = await self.subscription_repository.get_by_id(SubscriptionId(query.subscription_id))

        if not subscription or subscription.user_id != UserId(UUID(query.user_jwt_data.id)):
            raise

        subscription_dto = SubscriptionDTO.from_entity(subscription)

        logger.debug(
            "Get subscription by id",
            extra={"subscription_id": query.subscription_id, "subscription": subscription_dto}
        )
        return subscription_dto