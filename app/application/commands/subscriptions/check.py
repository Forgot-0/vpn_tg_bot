from dataclasses import dataclass
from uuid import UUID

from aiogram import Bot

from application.commands.base import BaseCommand, BaseCommandHandler
from infra.payments.base import BasePaymentService
from infra.repositories.subscriptions.base import BaseSubscriptionRepository



@dataclass(frozen=True)
class CheckPaySubCommand(BaseCommand):
    payment_id: str



@dataclass(frozen=True)
class CheckPaySubCommandHandler(BaseCommandHandler[CheckPaySubCommand, None]):
    payment_service: BasePaymentService
    subscription_repository: BaseSubscriptionRepository
    bot: Bot

    async def handle(self, command: CheckPaySubCommand) -> None:
        metadata = await self.payment_service.check(payment_id=command.payment_id)

        if not metadata: 
            raise

        subscription = await self.subscription_repository.get_by_id(id=UUID(metadata['subscription_id']))
        if subscription.vpn_url:
            await self.bot.send_message(
                chat_id=metadata['tg_id'],
                text=f'`{subscription.vpn_url}`',
                parse_mode='MarkDownV2'
            )