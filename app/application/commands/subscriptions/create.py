from dataclasses import dataclass
import logging
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from application.dtos.payments.url import PaymentDTO
from domain.entities.payment import Payment
from domain.entities.subscription import Subscription
from domain.repositories.payment import BasePaymentRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from domain.services.subscription import SubscriptionPricingService
from domain.values.servers import ProtocolType, Region
from infrastructure.payments.base import BasePaymentService


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateSubscriptionCommand(BaseCommand):
    telegram_id: int
    duration: int
    device_count: int
    protocol_types: list[str]


@dataclass(frozen=True)
class CreateSubscriptionCommandHandler(BaseCommandHandler[CreateSubscriptionCommand, PaymentDTO]):
    user_repository: BaseUserRepository
    payment_repository: BasePaymentRepository
    server_repository: BaseServerRepository
    subscription_repository: BaseSubscriptionRepository
    subs_price_service: SubscriptionPricingService
    payment_service: BasePaymentService

    async def handle(self, command: CreateSubscriptionCommand) -> PaymentDTO:
        server = await self.server_repository.get_by_max_free()

        if not server:
            raise

        user = await self.user_repository.get_by_telegram_id(telegram_id=command.telegram_id)
        if not user:
            raise 

        subscription = Subscription(
            duration=command.duration,
            device_count=command.device_count,
            server_id=server.id,
            region=Region(
                flag=server.region.flag,
                name=server.region.name,
                code=server.region.code
            ),
            user_id=user.id,
            protocol_types=[ProtocolType(t) for t in command.protocol_types]
        )

        await self.subscription_repository.create(subscription=subscription)

        payment = Payment.create(
            subscription=subscription,
            user_id=user.id,
            price=self.subs_price_service.calculate(subscription)
        )

        url, payment_id = await self.payment_service.create(order=payment)
        payment.payment_id = UUID(payment_id)

        await self.payment_repository.create(payment=payment)

        await self.mediator.publish(
            user.pull_events()+payment.pull_events()+subscription.pull_events()+server.pull_events()
        )

        logger.info("Create subscription", extra={"subscription": subscription})

        return PaymentDTO(url, payment.total_price)