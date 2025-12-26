from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import ForbiddenException
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.values.users import UserId, UserRole

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetSubscriptionsUserQuery(BaseQuery):
    user_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetSubscriptionsUserQueryHandler(BaseQueryHandler[GetSubscriptionsUserQuery, list[SubscriptionDTO]]):
    subscription_repository: BaseSubscriptionRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetSubscriptionsUserQuery) -> list[SubscriptionDTO]:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ) and UUID(query.user_jwt_data.id) != query.user_id:
            raise ForbiddenException()

        subscriptions = await self.subscription_repository.get_by_user(
            user_id=UserId(query.user_id)
        )

        subscriptions_dto = [SubscriptionDTO.from_entity(subscription) for subscription in subscriptions]

        logger.debug(
            "Get subscription by id",
            extra={"user_id": query.user_jwt_data.id, "subscriptions": subscriptions_dto}
        )
        return subscriptions_dto

