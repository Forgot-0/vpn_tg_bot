from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.filters.pagination import Pagination
from app.domain.filters.sort import SortDirection
from app.domain.filters.user import UserFilter
from app.presentation.schemas.filters import FilterMapper


class GetUsersRequest(BaseModel):
    telegram_id: int | None = None
    role: str | None = None
    is_premium: bool | None = None
    username: str | None = None
    fullname: str | None = None
    phone: str | None = None
    referred_by_id: str | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    has_subscriptions: bool | None = None
    min_referrals_count: int | None = Field(None, ge=0)

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    sort: str | None = (
        Field(None, examples=["created_at:desc,username:asc,id:desc"])
    )

    def to_user_filter(self) -> UserFilter:
        user_filter = UserFilter(
            telegram_id=self.telegram_id,
            role=self.role,
            is_premium=self.is_premium,
            username=self.username,
            fullname=self.fullname,
            phone=self.phone,
            referred_by_id=self.referred_by_id,
            created_after=self.created_after,
            created_before=self.created_before,
            has_subscriptions=self.has_subscriptions,
            min_referrals_count=self.min_referrals_count
        )

        pagination = Pagination(page=self.page, page_size=self.page_size)
        user_filter.set_pagination(pagination)

        sort_fields = FilterMapper.parse_sort_string(self.sort)
        for sort_field in sort_fields:
            user_filter.add_sort(sort_field.field, sort_field.direction)

        return user_filter
