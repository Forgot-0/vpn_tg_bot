
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal
from uuid import UUID


from app.application.dtos.base import BaseDTO
from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.domain.entities.user import User
from app.domain.services.utils import now_utc
from app.presentation.schemas.filters import FilterParam, ListParams, SortParam



@dataclass
class UserDTO(BaseDTO):
    id: UUID

    telegram_id: int | None = field(default=None)

    is_premium: bool = field(default=False)
    username: str | None = field(default=None)
    fullname: str | None = field(default=None)
    phone: str | None = field(default=None)

    referred_by: UUID | None = field(default=None)
    referrals_count: int = field(default=0)

    created_at: datetime = field(default_factory=now_utc)

    subscriptions: list[SubscriptionDTO] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'UserDTO':
        return UserDTO(
            id=UUID(data['id']) if isinstance(data['id'], str) else data['id'],
            telegram_id=data['telegram_id'],
            is_premium=data['is_premium'],
            username=data['username'],
            fullname=data['fullname'],
            phone=data['phone'],
            referred_by=UUID(data['referred_by']) if isinstance(data['referred_by'], str) else data['referred_by'],
            referrals_count=data['referrals_count'],
            created_at=data['created_at'],
            subscriptions=[SubscriptionDTO.from_dict(subscription) for subscription in data['subscriptions']],
        )

    @classmethod
    def from_entity(cls, entity: User) -> 'UserDTO':
        return UserDTO(
            id=entity.id.value,
            telegram_id=entity.telegram_id,
            is_premium=entity.is_premium,
            username=entity.username,
            fullname=entity.fullname,
            phone=entity.phone,
            referred_by=entity.referred_by.value if entity.referred_by else None,
            referrals_count=entity.referrals_count,
            created_at=entity.created_at,
            subscriptions=[SubscriptionDTO.from_entity(subscription) for subscription in entity.subscriptions],
        )


@dataclass
class UserSortParam(SortParam):
    field: Literal["id", "username", "created_at", "referrals_count", "telegram_id"]


@dataclass
class UserFilterParam(FilterParam):
    field: Literal["id", "username", "telegram_id", "referred_by", "fullname"]


@dataclass
class UserListParams(ListParams):
    sort: list[UserSortParam] | None = field(default=None)
    filters: list[UserFilterParam] | None = field(default=None)


