from dataclasses import dataclass
import logging

from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.repositories.users import BaseUserRepository

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetByTgIdQuery(BaseQuery):
    telegram_id: int


@dataclass(frozen=True)
class GetByTgIdQueryHandler(BaseQueryHandler[GetByTgIdQuery, list[SubscriptionDTO]]):
    user_repository: BaseUserRepository
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, query: GetByTgIdQuery) -> list[SubscriptionDTO]:
        user = await self.user_repository.get_by_telegram_id(telegram_id=query.telegram_id)
        if not user: raise
        subscriptions = await self.subscription_repository.get_by_user(user_id=user.id)

        subscriptions_dto = [SubscriptionDTO.from_entity(subscription) for subscription in subscriptions]

        logger.debug(
            "Get subscription by tg id",
            extra={"tg_id": query.telegram_id, "subscriptions": subscriptions_dto}
        )
        return subscriptions_dto