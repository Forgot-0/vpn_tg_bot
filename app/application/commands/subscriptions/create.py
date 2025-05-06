from dataclasses import dataclass
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.order import Order, PaymentStatus
from domain.entities.subscription import Subscription
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from domain.values.servers import ProtocolType, Region
from infrastructure.payments.base import BasePaymentService


@dataclass(frozen=True)
class CreateSubscriptionCommand(BaseCommand):
    telegram_id: int
    duration: int
    device_count: int
    flag: str
    name: str
    code: str
    protocol_types: list[str]


@dataclass(frozen=True)
class CreateSubscriptionCommandHandler(BaseCommandHandler[CreateSubscriptionCommand, str]):
    user_repository: BaseUserRepository
    order_repository: BaseOrderRepository
    server_repository: BaseServerRepository
    subscription_repository: BaseSubscriptionRepository
    payment_service: BasePaymentService

    async def handle(self, command: CreateSubscriptionCommand) -> str:
        server = await self.server_repository.get_by_max_free()

        if not server:
            raise

        subscription = Subscription(
            duration=command.duration,
            device_count=command.device_count,
            server_id=server.id,
            region=Region(
                flag=command.flag,
                name=command.name,
                code=command.code
            ),
            protocol_types=[ProtocolType(t) for t in command.protocol_types]
        )
        user = await self.user_repository.get_by_telegram_id(telegram_id=command.telegram_id)

        if not user:
            raise 

        user.subscriptions.append(subscription)
        await self.user_repository.update(user=user)
        await self.subscription_repository.create(subscription=subscription)

        order = Order.create(
            subscription=subscription,
            user_id=user.id,
        )

        url, payment_id = await self.payment_service.create(order=order)
        order.payment_id = UUID(payment_id)

        await self.order_repository.create(order=order)

        return url