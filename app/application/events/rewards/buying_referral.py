from dataclasses import dataclass

from application.events.base import BaseEventHandler
from domain.events.orders.paid import PaidOrderEvent
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.users import BaseUserRepository
from domain.services.rewards import RewardService


@dataclass(frozen=True)
class BuyingReferralEventHandler(BaseEventHandler[PaidOrderEvent, None]):
    reward_service: RewardService
    user_repository: BaseUserRepository
    order_repository: BaseOrderRepository

    async def handle(self, event: PaidOrderEvent) -> None:
        user = await self.user_repository.get_by_id(id=event.user_id)

        if not user.referred_by:
            return

        order = await self.order_repository.get_by_id(id=event.order_id)

        await self.reward_service.set_rewards_for_buy_referral(
            user_id=user.referred_by,
            order=order
        )