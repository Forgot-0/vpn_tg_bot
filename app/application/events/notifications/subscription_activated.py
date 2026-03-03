import logging
from dataclasses import dataclass

from app.application.events.base import BaseEventHandler
from app.application.services.notifications import NotificationSevice
from app.domain.events.paymens.paid import PaidPaymentEvent
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SendSubscriptionActivatedNotificationEventHandler(BaseEventHandler[PaidPaymentEvent, None]):
    notification_service: NotificationSevice
    user_repository: BaseUserRepository
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, event: PaidPaymentEvent) -> None:
        user = await self.user_repository.get_by_id(UserId(event.user_id))
        subscription = await self.subscription_repository.get_by_id(
            SubscriptionId(event.subscription_id)
        )

        if not user or not subscription:
            logger.warning(
                "Cannot send activation notification: user or subscription not found",
                extra={"user_id": event.user_id, "subscription_id": event.subscription_id}
            )
            return

        await self.notification_service.send_subscription_activated(
            user=user,
            subscription=subscription,
        )

        logger.info(
            "Sent subscription activated notification",
            extra={"user_id": event.user_id, "subscription_id": event.subscription_id}
        )