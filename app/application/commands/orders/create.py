from dataclasses import dataclass
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.order import Order
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.services.discounts import DiscountService
from infrastructure.payments.base import BasePaymentService


@dataclass(frozen=True)
class CreateOrderCommand(BaseCommand):
    subscription_id: UUID
    user_id: int


@dataclass(frozen=True)
class CreateOrderCommandHandler(BaseCommandHandler[CreateOrderCommand, tuple[Order, str]]):
    order_repository: BaseOrderRepository
    discount_service: DiscountService
    subscription_repository: BaseSubscriptionRepository
    payment_service: BasePaymentService

    async def handle(self, command: CreateOrderCommand) -> tuple[Order, str]:

        subscription = await self.subscription_repository.get_by_id(id=command.subscription_id)

        await self.discount_service.set_discounts(user_id=command.user_id, subscriptions=[subscription])

        order = Order.create(
            subscription=subscription,
            user_id=command.user_id,
            discount=subscription.discount
        )

        url, payment_id = await self.payment_service.create(order=order)

        order.payment_id = payment_id
        await self.order_repository.create(order=order)

        await self.mediator.publish(order.pull_events())

        return url