from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.users.referred import ReferredUserEvent
from domain.repositories.users import BaseUserRepository


@dataclass(frozen=True)
class ReferredUserEventHandler(BaseEventHandler[ReferredUserEvent, None]):
    user_repository: BaseUserRepository

    async def handle(self, event: ReferredUserEvent) -> None:
        user = await self.user_repository.get_by_id(id=event.referred_by)
        user.assignReferral(referral_id=event.referral_id)
        await self.user_repository.update(user=user)
        await self.mediator.publish(user.pull_events())