from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.domain.entities.subscription import SubscriptionStatus
from app.domain.repositories.servers import BaseServerRepository
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.servers import VPNConfig
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId
from app.infrastructure.builders_params.factory import ProtocolBuilderFactory


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetConfigQuery(BaseQuery):
    subscription_id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetConfigQueryHandler(BaseQueryHandler[GetConfigQuery, VPNConfig]):
    subscription_repository: BaseSubscriptionRepository
    user_repositry: BaseUserRepository
    server_reposiotry: BaseServerRepository
    builder_factory: ProtocolBuilderFactory

    async def handle(self, query: GetConfigQuery) -> VPNConfig:
        subscription = await self.subscription_repository.get_by_id(SubscriptionId(query.subscription_id))
        if not subscription:
            raise

        if query.user_jwt_data.role != "admin" and UserId(UUID(query.user_jwt_data.id)) != subscription.user_id:
            raise

        if subscription.status != SubscriptionStatus.ACTIVE:
            raise

        server = await self.server_reposiotry.get_by_id(subscription.server_id)
        user = await self.user_repositry.get_by_id(subscription.user_id)

        if not user or not server:
            raise

        builder = self.builder_factory.get(server.api_type, subscription.protocol_types[0])
        config = builder.builde_config_vpn(user, subscription, server)

        logger.debug(
            "Get config subscription",
            extra={"subscription_id": query.subscription_id, "config": config}
        )
        return config