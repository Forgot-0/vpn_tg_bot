from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from domain.entities.base import AggregateRoot
from domain.entities.discount import Discount
from domain.entities.subscription import Subscription



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
    user_id: int
    is_received: bool = field(default=False)

    def __hash__(self) -> int:
        return hash(self.reward_id)

    def __eq__(self, other):
        return isinstance(other, RewardUser) and self.reward_id == other.reward_id and self.user_id == other.user_id
