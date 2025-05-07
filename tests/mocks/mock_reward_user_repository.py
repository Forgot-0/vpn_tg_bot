from typing import List, Optional
from uuid import UUID
from domain.entities.reward import RewardUser
from domain.repositories.rewards import BaseRewardUserRepository
from domain.values.users import UserId

class MockRewardUserRepository(BaseRewardUserRepository):
    def __init__(self):
        self._data: dict[tuple[UUID, UserId], RewardUser] = {}

    async def create(self, reward_user: RewardUser) -> None:
        key = (reward_user.reward_id, reward_user.user_id)
        self._data[key] = reward_user

    async def get_by_reward_user(self, reward_id: UUID, user_id: UserId) -> Optional[RewardUser]:
        return self._data.get((reward_id, user_id))

    async def get_not_received_by_user(self, user_id: int) -> List[RewardUser]:
        return [ru for ru in self._data.values()
                if ru.user_id == user_id and not ru.count]

    async def receive(self, reward_id: UUID, user_id: UserId) -> None:
        key = (reward_id, user_id)
        if key in self._data:
            ru = self._data[key]
            ru.count -= 1
            self._data[key] = ru