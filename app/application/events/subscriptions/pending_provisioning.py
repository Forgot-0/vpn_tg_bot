from dataclasses import dataclass
import logging

from app.application.commands.provisioning.provision_access import (
    ProvisionSubscriptionAccessCommand,
    ProvisionSubscriptionAccessHandler,
)
from app.application.events.base import BaseEventHandler
from app.domain.events.subscriptions import SubscriptionPendingProvisioningEvent


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SubscriptionPendingProvisioningHandler(
    BaseEventHandler[SubscriptionPendingProvisioningEvent, None]
):
    provision_handler: ProvisionSubscriptionAccessHandler

    async def handle(self, event: SubscriptionPendingProvisioningEvent) -> None:
        try:
            await self.provision_handler.handle(
                ProvisionSubscriptionAccessCommand(subscription_id=event.subscription_id)
            )
        except Exception:
            logger.exception(
                "Failed to provision subscription %s",
                event.subscription_id,
            )
