from dataclasses import dataclass
from datetime import datetime
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.payments.url import PaymentDTO
from app.domain.entities.payment import Payment
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.repositories.servers import BaseServerRepository
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.repositories.users import BaseUserRepository
from app.domain.services.subscription import SubscriptionPricingService
from app.domain.values.subscriptions import SubscriptionId
from app.infrastructure.payments.base import BasePaymentService


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RenewSubscriptionCommand(BaseCommand):
    subscription_id: UUID
    duration: int


@dataclass(frozen=True)
class RenewSubscriptionCommandHandler(BaseCommandHandler[RenewSubscriptionCommand, PaymentDTO]):
    user_repository: BaseUserRepository
    payment_repository: BasePaymentRepository
    server_repository: BaseServerRepository
    subscription_repository: BaseSubscriptionRepository
    subs_price_service: SubscriptionPricingService
    payment_service: BasePaymentService

    async def handle(self, command: RenewSubscriptionCommand) -> PaymentDTO:
        subscription = await self.subscription_repository.get_by_id(id=SubscriptionId(command.subscription_id))
        if not subscription: raise

        current_price = self.subs_price_service.calculate(subscription)

        subscription.renew(command.duration)
        new_price = abs(current_price - self.subs_price_service.calculate(subscription))
        payment = Payment.create(
            subscription=subscription,
            user_id=subscription.user_id,
            price=new_price
        )

        url, payment_id = await self.payment_service.create(order=payment)
        payment.payment_id = UUID(payment_id)

        await self.payment_repository.create(payment=payment)
        await self.mediator.publish(subscription.pull_events())
        logger.info("Renew subscription", extra={"subscription": subscription})

        return PaymentDTO(url=url, price=new_price)