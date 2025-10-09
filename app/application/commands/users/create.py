from dataclasses import dataclass
import logging
from uuid import UUID

from application.commands.base import BaseCommand, BaseCommandHandler
from domain.entities.user import User
from domain.repositories.users import BaseUserRepository
from domain.values.users import UserId
from infrastructure.mediator.event import BaseEventBus


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    tg_id: int
    is_premium: bool | None
    username: str | None
    fullname: str | None
    phone: str | None
    referred_by: str | None


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler[CreateUserCommand, None]):
    user_repository: BaseUserRepository
    event_bus: BaseEventBus

    async def handle(self, command: CreateUserCommand) -> None:
        user = await self.user_repository.get_by_telegram_id(telegram_id=command.tg_id)
        if user: return 

        user = User.create(
            telegram_id=command.tg_id,
            is_premium=command.is_premium,
            username=command.username,
            fullname=command.fullname,
            phone=command.phone,
            referred_by=UserId(UUID(command.referred_by)) if command.referred_by else None
        )

        await self.user_repository.create(user=user)
        await self.event_bus.publish(user.pull_events())
        logger.info("Create user", extra={"user": user})