from dataclasses import dataclass
from uuid import UUID

from domain.entities.order import Order
from domain.entities.reward import Reward, RewardUser
from domain.exception.base import NotFoundRewardsException
from domain.repositories.rewards import BaseRewardRepository, BaseRewardUserRepository
from domain.repositories.users import BaseUserRepository


@dataclass
class RewardService:
    reward_repository: BaseRewardRepository
    reward_user_repository: BaseRewardUserRepository
    user_repository: BaseUserRepository


    async def _set_user_reward(self, reward_id: UUID, user_id: int) -> None:
        reward_user = RewardUser(
            reward_id=reward_id,
            user_id=user_id,
        )
        await self.reward_user_repository.create(reward_user=reward_user)


    async def set_rewards_for_buy_referral(self, user_id: int, order: Order) -> None:
        reward = await self.reward_repository.get_by_conditions(
            {
                "conditions.buy_subscription": order.subscription.id
            }
        )

        if reward:
            await self._set_user_reward(reward_id=reward.id, user_id=user_id)

    async def set_rewards_for_referral(self, user_id: int) -> None:
        user = await self.user_repository.get_by_id(id=user_id)

        if user.referrals_count % 10 != 0:
            return

        reward = await self.reward_repository.get_by_conditions(
            {
                "conditions.referrals_count": user.referrals_count
            }
        )

        if reward:
            await self._set_user_reward(reward_id=reward.id, user_id=user_id)

    async def set_reward_for_trial_period(self, user_id: int) -> None:
        reward = await self.reward_repository.get_by_conditions(
            {
                "conditions.trial": True
            }
        )

        if reward:
            await self._set_user_reward(reward_id=reward.id, user_id=user_id)

    async def receive_reward(self, user_id: int, reward_id: UUID) -> Reward:
        await self.reward_user_repository.receive(
            reward_id=reward_id,
            user_id=user_id
        )
        reward = await self.reward_repository.get_by_id(id=reward_id)
        return reward

    async def get_rewerds_user(self, user_id: int) -> list[Reward]:
        rewads_user = await self.reward_user_repository.get_not_received_by_user(
            user_id=user_id
        )

        if rewads_user is None:
            raise NotFoundRewardsException()

        rewards = []

        for rewar_user in rewads_user:
            rewards.append(
                await self.reward_repository.get_by_id(id=rewar_user.reward_id)
            )

        return rewards
