from dataclasses import dataclass

from application.commands.base import BaseCommand, BaseCommandHandler
from infra.repositories.subscriptions.base import BaseSubscriptionRepository


@dataclass(frozen=True)
class PaidSubscriptionCommand(BaseCommand):
    tg_id: int


@dataclass(frozen=True)
class PaidSubscriptionCommandHandler(BaseCommandHandler[PaidSubscriptionCommand, None]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, command: PaidSubscriptionCommand) -> None:
        subscription = await self.subscription_repository.get_by_tg_id(tg_id=command.tg_id)
        subscription.paid()
        await self.subscription_repository.pay(id=subscription.id)
        await self.mediator.publish(subscription.pull_events())