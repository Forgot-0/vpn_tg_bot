from dataclasses import dataclass

from application.dtos.subsciprions.subscription import SubscriptionDTO
from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.users import BaseUserRepository



@dataclass(frozen=True)
class GetByTgIdQuery(BaseQuery):
    telegram_id: int


@dataclass(frozen=True)
class GetByTgIdQueryHandler(BaseQueryHandler[GetByTgIdQuery, list[SubscriptionDTO]]):
    user_repository: BaseUserRepository

    async def handle(self, query: GetByTgIdQuery) -> list[SubscriptionDTO]:
        user = await self.user_repository.get_by_telegram_id(telegram_id=query.telegram_id)
        if not user: raise

        return [SubscriptionDTO.from_entity(subscription) for subscription in user.subscriptions]