from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from domain.entities.order import Order
from domain.entities.reward import Reward, RewardUser
from domain.entities.subscription import Subscription
from domain.repositories.rewards import BaseRewardRepository, BaseRewardUserRepository
from domain.repositories.users import BaseUserRepository


@dataclass
class RewardService:
    reward_repository: BaseRewardRepository
    reward_user_repository: BaseRewardUserRepository
    user_repository: BaseUserRepository

    async def set_rewards_for_buy_referral(self, user_id: int, order: Order) -> None:
        reward = Reward(
                name='За покупку реферала',
                description="",
                conditions={},
                present=Subscription(
                    name='Present',
                    description='',
                    price=0,
                    duration=timedelta(days=order.subscription.duration.days//10)
                )
            )

        await self.reward_repository.create(reward=reward)
        reward_user = RewardUser(
            reward_id=reward.id,
            user_id=user_id,
        )
        await self.reward_user_repository.create(reward_user=reward_user)

    async def set_rewards_for_referral(self, user_id: int) -> None:
        user = await self.user_repository.get_by_id(id=user_id)

        rewards = await self.reward_repository.get()

        user_rewerds = await self.reward_user_repository.get_by_user(user_id=user_id)

        for reward in rewards:
            if reward in user_rewerds:
                continue
            conditions = reward.conditions


            if 'count_referrals' in conditions and user.referrals_count >= conditions['count_referrals']:
                reward_user = RewardUser(
                    reward_id=reward.id,
                    user_id=user_id,
                )
                await self.reward_user_repository.create(reward_user=reward_user)

        await self.user_repository.update(user=user)

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

        rewards = []

        for rewar_user in rewads_user:
            rewards.append(
                await self.reward_repository.get_by_id(id=rewar_user.reward_id)
            )

        return rewards
