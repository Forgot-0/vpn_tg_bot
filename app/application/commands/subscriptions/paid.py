from dataclasses import dataclass
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from application.exeption import NotFoundException
from infra.repositories.subscriptions.base import BaseSubscriptionRepository


@dataclass(frozen=True)
class PaidSubscriptionCommand(BaseCommand):
    tg_id: int
    payment_id: str
    subscription_id: str


@dataclass(frozen=True)
class PaidSubscriptionCommandHandler(BaseCommandHandler[PaidSubscriptionCommand, None]):
    subscription_repository: BaseSubscriptionRepository

    async def handle(self, command: PaidSubscriptionCommand) -> None:
        subscription = await self.subscription_repository.get_by_id(id=UUID(command.subscription_id))
        if not subscription: raise NotFoundException('Not Found Sub')
        subscription.paid()
        await self.subscription_repository.pay(id=subscription.id)
        await self.mediator.publish(subscription.pull_events())
