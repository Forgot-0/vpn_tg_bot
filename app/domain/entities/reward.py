from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from app.domain.entities.base import AggregateRoot
from app.domain.entities.subscription import Subscription
from app.domain.values.users import UserId



@dataclass
class Reward(AggregateRoot):
    id: UUID = field(default_factory=uuid4, kw_only=True)
    name: str
    description: str
    conditions: dict[str, Any]
    present: Subscription

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, value: UUID) -> bool:
        return self.id == value


@dataclass
class RewardUser(AggregateRoot):
    reward_id: UUID
    user_id: UserId
    count: int = field(default=0)

    def __hash__(self) -> int:
        return hash(self.reward_id)

    def __eq__(self, other):
        return isinstance(other, RewardUser) and self.reward_id == other.reward_id and self.user_id == other.user_id
