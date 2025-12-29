from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from app.domain.filters.pagination import Pagination
from app.domain.filters.subscription import SubscriptionFilter
from app.presentation.schemas.filters import FilterMapper


class CreateSubscriptionRequests(BaseModel):
    duration_days: int
    device_count: int
    protocol_types: list[str]


class RenewSubscriptionRequests(BaseModel):
    duration_days: int



class GetSubscriptionsRequest(BaseModel):
    user_id: UUID | None = None
    server_id: UUID | None = None
    region_code: str | None = None
    status: str | None = None
    protocol_types: list[str] | None = None
    min_duration: int | None = Field(None, ge=1)
    max_duration: int | None = None
    start_date_after: datetime | None = None
    start_date_before: datetime | None = None
    min_device_count: int | None = Field(None, ge=1)
    max_device_count: int | None = None

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    sort: str | None = (
        Field(None, examples=["created_at:desc,username:asc,id:desc"])
    )

    def to_subscription_filter(self) -> SubscriptionFilter:
        subscription_filter = SubscriptionFilter(
            user_id=self.user_id,
            server_id=self.server_id,
            region_code=self.region_code,
            status=self.status,
            protocol_types=self.protocol_types,
            min_duration=self.min_duration,
            max_duration=self.max_duration,
            start_date_after=self.start_date_after,
            start_date_before=self.start_date_before,
            min_device_count=self.min_device_count,
            max_device_count=self.max_device_count
        )

        pagination = Pagination(page=self.page, page_size=self.page_size)
        subscription_filter.set_pagination(pagination)

        sort_fields = FilterMapper.parse_sort_string(self.sort)
        for sort_field in sort_fields:
            subscription_filter.add_sort(sort_field.field, sort_field.direction)

        return subscription_filter
