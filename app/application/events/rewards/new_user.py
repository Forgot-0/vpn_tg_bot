from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.users.created import NewUserEvent
from domain.services.rewards import RewardService


@dataclass(frozen=True)
class TrialRewardEventHandler(BaseEventHandler[NewUserEvent, None]):
    reward_service: RewardService

    async def handle(self, event: NewUserEvent) -> None:
        await self.reward_service.set_reward_for_trial_period(
            user_id=event.user_id
        )