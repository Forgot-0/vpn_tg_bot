from dataclasses import dataclass

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.subscription import ProductType, Subscription
from infra.repositories.subscriptions.base import BaseSubscriptionRepository


@dataclass(frozen=True)
class CreateSubscriptionCommand(BaseCommand):
    tg_id: int
    product: int


@dataclass(frozen=True)
class CreateSubscriptionCommandHandler(BaseCommandHandler[CreateSubscriptionCommand, Subscription]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, command: CreateSubscriptionCommand) -> Subscription:
        subscription = Subscription.create(
            tg_id=command.tg_id,
            product=ProductType(command.product)
        )

        await self.subscription_repository.create(subscription=subscription)
        await self.mediator.publish(subscription.pull_events())
        return subscription