from dataclasses import dataclass
import logging
from uuid import UUID

from application.queries.base import BaseQuery, BaseQueryHandler
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from domain.values.servers import VPNConfig
from domain.values.subscriptions import SubscriptionId
from infrastructure.builders_params.factory import ProtocolBuilderFactory


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetConfigQuery(BaseQuery):
    subscription_id: UUID


@dataclass(frozen=True)
class GetConfigQueryHandler(BaseQueryHandler[GetConfigQuery, VPNConfig]):
    subscription_repository: BaseSubscriptionRepository
    user_repositry: BaseUserRepository
    server_reposiotry: BaseServerRepository
    builder_factory: ProtocolBuilderFactory

    async def handle(self, query: GetConfigQuery) -> VPNConfig:
        subscription = await self.subscription_repository.get_by_id(SubscriptionId(query.subscription_id))
        server = await self.server_reposiotry.get_by_id(subscription.server_id)
        user = await self.user_repositry.get_by_id(subscription.user_id)

        if not user or not server or not subscription: raise

        builder = self.builder_factory.get(server.api_type, subscription.protocol_types[0])
        config = builder.builde_config_vpn(user, subscription, server)

        logger.debug(
            "Get config subscription",
            extra={"subscription_id": query.subscription_id, "config": config}
        )
        return config