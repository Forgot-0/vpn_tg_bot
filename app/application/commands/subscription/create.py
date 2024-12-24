from dataclasses import dataclass, field
from datetime import timedelta

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.subscription import Subscription
from domain.repositories.subscriptions import BaseSubscriptionRepository


@dataclass(frozen=True)
class CreateSubscriptionCommnad(BaseCommand):
    name: str
    description: str
    duration: timedelta
    price: float
    is_active: bool = field(default=False)
    limit_ip: int = field(default=1)
    limit_trafic: int = field(default=0)


@dataclass(frozen=True)
class CreateSubscriptionCommnadHandler(BaseCommandHandler[CreateSubscriptionCommnad, None]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, command: CreateSubscriptionCommnad) -> None:
        subscription = Subscription(
            name=command.name,
            description=command.description,
            duration=command.duration,
            price=command.price,
            limit_ip=command.limit_ip,
            limit_trafic=command.limit_trafic
        )

        await self.subscription_repository.create(subscription=subscription)

        await self.mediator.publish(subscription.pull_events())
