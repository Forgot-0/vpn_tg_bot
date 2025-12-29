from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from app.domain.filters.pagination import Pagination
from app.domain.filters.payment import PaymentFilter
from app.presentation.schemas.filters import FilterMapper


class GetPaymentsRequest(BaseModel):
    user_id: UUID | None = None
    subscription_id: UUID | None = None
    status: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    payment_date_after: datetime | None = None
    payment_date_before: datetime | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    has_payment_id: bool | None = None

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    sort: str | None = (
        Field(None, examples=["created_at:desc,username:asc,id:desc"])
    )

    def to_payment_filter(self) -> PaymentFilter:
        payment_filter = PaymentFilter(
            user_id=self.user_id,
            subscription_id=self.subscription_id,
            status=self.status,
            min_price=self.min_price,
            max_price=self.max_price,
            payment_date_after=self.payment_date_after,
            payment_date_before=self.payment_date_before,
            created_after=self.created_after,
            created_before=self.created_before,
            has_payment_id=self.has_payment_id
        )

        pagination = Pagination(page=self.page, page_size=self.page_size)
        payment_filter.set_pagination(pagination)

        sort_fields = FilterMapper.parse_sort_string(self.sort)
        for sort_field in sort_fields:
            payment_filter.add_sort(sort_field.field, sort_field.direction)

        return payment_filter