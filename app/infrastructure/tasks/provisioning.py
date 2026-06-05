from dataclasses import dataclass
import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.application.commands.provisioning.provision_access import (
    ProvisionSubscriptionAccessCommand,
    ProvisionSubscriptionAccessHandler,
)
from app.application.interfaces.queue import BaseTask


logger = logging.getLogger(__name__)


@dataclass
class ProvisionSubscriptionTask(BaseTask):
    __task_name__ = "provisioning.provision_subscription"

    @staticmethod
    @inject
    async def run(
        subscription_id: str,
        handler: FromDishka[ProvisionSubscriptionAccessHandler],
    ) -> None:
        try:
            await handler.handle(
                ProvisionSubscriptionAccessCommand(subscription_id=UUID(subscription_id))
            )
        except Exception:
            logger.exception(
                "Background provisioning failed for subscription %s",
                subscription_id,
            )
