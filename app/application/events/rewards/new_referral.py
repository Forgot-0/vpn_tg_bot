from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.users.referred import ReferralAssignedEvent
from domain.services.rewards import RewardService


@dataclass(frozen=True)
class CheckNewRewardEventHandler(BaseEventHandler[ReferralAssignedEvent, None]):
    reward_service: RewardService

    async def handle(self, event: ReferralAssignedEvent) -> None:
        await self.reward_service.set_rewards_for_referral(
            user_id=event.user_id
        )