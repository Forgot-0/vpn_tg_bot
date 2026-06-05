from dataclasses import dataclass
import logging

from app.application.commands.base import BaseCommand, BaseCommandHandler
from app.application.event_bus import EventBus
from app.domain.entities.user import User
from app.domain.repositories.uow import UnitOfWork
from app.domain.repositories.users import UserRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RegisterUserByTelegramCommand(BaseCommand):
    telegram_id: int
    referral_code: str


@dataclass(frozen=True)
class RegisterUserByTelegramCommandHandler(BaseCommandHandler[RegisterUserByTelegramCommand, None]):
    user_repository: UserRepository
    uow: UnitOfWork
    event_bus: EventBus

    async def handle(self, command: RegisterUserByTelegramCommand) -> None:
        reffered_user_id = None
        if command.referral_code is not None:
            reffered_user = await self.user_repository.get_by_referral_code(
                command.referral_code
            )
            if reffered_user is not None:
                reffered_user.increment_referrals()
                reffered_user_id = reffered_user.id
                await self.user_repository.update(reffered_user)

        user = User.create(
            telegram_id=command.telegram_id,
            referred_by=reffered_user_id
        )

        await self.user_repository.add(user)
        await self.uow.commit()
        await self.event_bus.publish(user.pull_events())

