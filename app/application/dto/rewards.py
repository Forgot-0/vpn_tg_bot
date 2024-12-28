from dataclasses import dataclass
from typing import Any

from application.dto.base import BaseDTO
from application.dto.subscription import SubscriptionDTO
from domain.entities.reward import Reward



@dataclass
class RewardDTO(BaseDTO):
    name: str
    description: str
    present: SubscriptionDTO

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'RewardDTO':
        ...

    @classmethod
    def from_entity(cls, reward: Reward) -> 'RewardDTO':
        return RewardDTO(
            name=reward.name,
            description=reward.description,
            present=SubscriptionDTO.from_entity(reward.present)
        )