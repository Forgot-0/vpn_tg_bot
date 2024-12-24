from dataclasses import dataclass
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.order import Order
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from infrastructure.payments.base import BasePaymentService


@dataclass(frozen=True)
class CreateOrderCommand(BaseCommand):
    subscription_id: UUID
    user_id: int


@dataclass(frozen=True)
class CreateOrderCommandHandler(BaseCommandHandler[CreateOrderCommand, tuple[Order, str]]):
    order_repository: BaseOrderRepository
    subscription_repository: BaseSubscriptionRepository
    server_reposiptry: BaseServerRepository
    payment_service: BasePaymentService

    async def handle(self, command: CreateOrderCommand) -> tuple[Order, str]:
        server = await self.server_reposiptry.get_by_max_free()
        if server.free <= 0: 
            raise

        subscription = await self.subscription_repository.get_by_id(id=command.subscription_id)
        order = Order.create(
            subscription=subscription,
            user_id=command.user_id,
            server_id=server.id
        )

        url, payment_id = await self.payment_service.create(order=order)

        order.payment_id = payment_id
        await self.order_repository.create(order=order)

        await self.mediator.publish(subscription.pull_events())

        return url