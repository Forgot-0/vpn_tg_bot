from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from application.dtos.payments.url import PaymentDTO
from domain.entities.payment import Payment
from domain.repositories.payment import BasePaymentRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from domain.services.subscription import SubscriptionPricingService
from domain.values.subscriptions import SubscriptionId
from infrastructure.payments.base import BasePaymentService


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

        if subscription.end_date < datetime.now():
            current_price = 0

        subscription.renew(command.duration)
        new_price = abs(current_price - self.subs_price_service.calculate(subscription))
        print(new_price, current_price, subscription, self.subs_price_service.calculate(subscription))
        payment = Payment.create(
            subscription=subscription,
            user_id=subscription.user_id,
            price=new_price
        )

        url, payment_id = await self.payment_service.create(order=payment)
        payment.payment_id = UUID(payment_id)

        await self.payment_repository.create(payment=payment)

        return PaymentDTO(url=url, price=new_price)