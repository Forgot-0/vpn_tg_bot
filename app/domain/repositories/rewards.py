from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.domain.entities.reward import Reward, RewardUser


@dataclass
class BaseRewardRepository(ABC):

    @abstractmethod
    async def create(self, reward: Reward) -> None: ...

    @abstractmethod
    async def get(self) -> list[Reward]: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Reward: ...

    @abstractmethod
    async def get_by_conditions(self, filters: dict[str, Any]) -> Reward: ...


@dataclass
class BaseRewardUserRepository(ABC):
    @abstractmethod
    async def create(self, reward_user: RewardUser) -> None: ...

    @abstractmethod
    async def get_by_reward_user(self, reward_id: UUID, user_id: int) -> RewardUser: ...

    @abstractmethod
    async def get_not_received_by_user(self, user_id: int) -> list[RewardUser]: ...

    @abstractmethod
    async def receive(self, reward_id: UUID, user_id: int) -> None: ...