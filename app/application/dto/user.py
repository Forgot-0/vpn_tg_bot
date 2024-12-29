from dataclasses import dataclass
from typing import Any

from application.dto.base import BaseDTO
from domain.entities.user import User


@dataclass
class UserDTO(BaseDTO):
    id: int
    referred_by: int | None
    referrals_count: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'UserDTO':
        return super().from_dict(data)

    @classmethod
    def from_entity(self, user: User) -> 'UserDTO':
        return UserDTO(
            id=user.id,
            referred_by=user.referred_by,
            referrals_count=user.referrals_count
        )