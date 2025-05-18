from dataclasses import dataclass

from application.dtos.subsciprions.subscription import SubscriptionDTO
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository



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

        return [SubscriptionDTO.from_entity(subscription) for subscription in subscriptions]