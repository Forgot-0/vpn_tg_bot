from dataclasses import dataclass
import logging
from uuid import UUID

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.dtos.payments.url import PaymentDTO
from app.application.dtos.users.jwt import UserJWTData
from app.domain.entities.payment import Payment
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.services.subscription import SubscriptionPricingService
from app.domain.values.subscriptions import SubscriptionId
from app.domain.values.users import UserId
from app.application.services.payment import BasePaymentService
from app.application.exception import NotFoundException, ForbiddenException


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RenewSubscriptionCommand(BaseCommand):
    subscription_id: UUID
    duration: int
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class RenewSubscriptionCommandHandler(BaseCommandHandler[RenewSubscriptionCommand, PaymentDTO]):
    payment_repository: BasePaymentRepository
    subscription_repository: BaseSubscriptionRepository
    subs_price_service: SubscriptionPricingService
    payment_service: BasePaymentService

    async def handle(self, command: RenewSubscriptionCommand) -> PaymentDTO:
        subscription = await self.subscription_repository.get_by_id(id=SubscriptionId(command.subscription_id))
        if not subscription:
            raise NotFoundException()

        if subscription.user_id != UserId(UUID(command.user_jwt_data.id)):
            raise ForbiddenException()

        current_price = self.subs_price_service.calculate(subscription)

        subscription.renew(command.duration)
        new_price = abs(current_price - self.subs_price_service.calculate(subscription))
        payment = Payment.create(
            subscription=subscription,
            user_id=subscription.user_id,
            price=new_price
        )

        payment_data = await self.payment_service.create(order=payment)
        payment.payment_id = payment_data.payment_id

        await self.payment_repository.create(payment=payment)
        logger.info("Renew subscription", extra={"subscription": subscription})

        return PaymentDTO(url=payment_data.url, price=new_price)