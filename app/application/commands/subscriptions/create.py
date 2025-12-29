from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.payments.url import PaymentData
from app.application.dtos.users.jwt import UserJWTData
from app.domain.entities.payment import Payment
from app.domain.entities.subscription import Subscription
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.repositories.servers import BaseServerRepository
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.repositories.users import BaseUserRepository
from app.domain.services.subscription import SubscriptionPricingService
from app.domain.values.servers import ProtocolType, Region
from app.domain.values.users import UserId
from app.infrastructure.mediator.event import BaseEventBus
from app.application.services.payment import BasePaymentService
from app.application.exception import NotFoundException


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateSubscriptionCommand(BaseCommand):
    duration: int
    device_count: int
    protocol_types: list[str]
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class CreateSubscriptionCommandHandler(BaseCommandHandler[CreateSubscriptionCommand, PaymentData]):
    payment_repository: BasePaymentRepository
    server_repository: BaseServerRepository
    subscription_repository: BaseSubscriptionRepository
    subs_price_service: SubscriptionPricingService
    payment_service: BasePaymentService
    event_bus: BaseEventBus

    async def handle(self, command: CreateSubscriptionCommand) -> PaymentData:
        protocol_types=[ProtocolType(t) for t in command.protocol_types]
        server = await self.server_repository.get_by_max_free(protocol_types)

        if not server:
            raise NotFoundException()

        subscription = Subscription(
            duration=command.duration,
            device_count=command.device_count,
            server_id=server.id,
            region=Region(
                flag=server.region.flag,
                name=server.region.name,
                code=server.region.code
            ),
            user_id=UserId(UUID(command.user_jwt_data.id)),
            protocol_types=protocol_types
        )

        payment = Payment.create(
            subscription=subscription,
            user_id=UserId(UUID(command.user_jwt_data.id)),
            price=self.subs_price_service.calculate(subscription)
        )

        payment_data = await self.payment_service.create(order=payment)
        payment.payment_id = payment_data.payment_id

        await self.payment_repository.create(payment=payment)

        await self.event_bus.publish(
            payment.pull_events()+subscription.pull_events()+server.pull_events()
        )

        logger.info("Create subscription", extra={"subscription": subscription})

        return PaymentData(payment_data.url, payment.total_price)