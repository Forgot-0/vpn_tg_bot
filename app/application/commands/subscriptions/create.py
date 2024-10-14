from dataclasses import dataclass

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.subscription import ProductType, Subscription
from infra.repositories.servers.base import BaseServerRepository
from infra.repositories.subscriptions.base import BaseSubscriptionRepository


@dataclass(frozen=True)
class CreateSubscriptionCommand(BaseCommand):
    tg_id: int
    product: int


@dataclass(frozen=True)
class CreateSubscriptionCommandHandler(BaseCommandHandler[CreateSubscriptionCommand, Subscription]):
    subscription_repository: BaseSubscriptionRepository
    server_reposiptry: BaseServerRepository

    async def handle(self, command: CreateSubscriptionCommand) -> Subscription:
        server = await self.server_reposiptry.get_by_max_free()
        if server.free <= 0: 
            raise

        subscription = Subscription.create(
            tg_id=command.tg_id,
            product=ProductType(command.product),
            server_id=server.id
        )

        await self.subscription_repository.delete_not_paid_sub(tg_id=command.tg_id)
        await self.subscription_repository.create(subscription=subscription)
        await self.mediator.publish(subscription.pull_events())
        return subscription