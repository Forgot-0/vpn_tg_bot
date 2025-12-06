from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.values.users import UserId

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetSubscriptionsUserQuery(BaseQuery):
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetSubscriptionsUserQueryHandler(BaseQueryHandler[GetSubscriptionsUserQuery, list[SubscriptionDTO]]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, query: GetSubscriptionsUserQuery) -> list[SubscriptionDTO]:
        subscriptions = await self.subscription_repository.get_by_user(
            user_id=UserId(UUID(query.user_jwt_data.id))
        )

        subscriptions_dto = [SubscriptionDTO.from_entity(subscription) for subscription in subscriptions]

        logger.debug(
            "Get subscription by tg id",
            extra={"tg_id": query.user_jwt_data.id, "subscriptions": subscriptions_dto}
        )
        return subscriptions_dto

