from typing import List, Any, Optional
from uuid import UUID
from domain.entities.reward import Reward
from domain.repositories.rewards import BaseRewardRepository


class MockRewardRepository(BaseRewardRepository):
    def __init__(self):
        self._data: dict[UUID, Reward] = {}

    async def create(self, reward: Reward) -> None:
        self._data[reward.id] = reward

    async def get(self) -> List[Reward]:
        return list(self._data.values())

    async def get_by_id(self, id: UUID) -> Optional[Reward]:
        return self._data.get(id)

    async def get_by_conditions(self, filters: dict[str, Any]) -> Optional[Reward]:
        for reward in self._data.values():
            if all(getattr(reward, key, None) == value for key, value in filters.items()):
                return reward
        return None