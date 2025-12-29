from pydantic import BaseModel, Field

from app.domain.filters.pagination import Pagination
from app.domain.filters.server import ServerFilter
from app.presentation.schemas.filters import FilterMapper


class CreateServerRequest(BaseModel):
    limit: int
    region_code: str

    ip: str
    panel_port: int
    panel_path: str
    domain: str | None

    username: str
    password: str
    twoFactorCode: str | None = Field(default=None)



class GetServersRequest(BaseModel):
    region_code: str| None = None
    api_type: str| None = None
    min_free_slots: int| None = Field(None, ge=1)
    max_free_slots: int| None = None
    protocol_types: list[str]| None = None
    has_domain: bool| None = None

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    sort: str | None = (
        Field(None, examples=["created_at:desc,username:asc,id:desc"])
    )

    def to_server_filter(self) -> ServerFilter:
        server_filter = ServerFilter(
            region_code=self.region_code,
            api_type=self.api_type,
            min_free_slots=self.min_free_slots,
            max_free_slots=self.max_free_slots,
            protocol_types=self.protocol_types,
            has_domain=self.has_domain
        )

        pagination = Pagination(page=self.page, page_size=self.page_size)
        server_filter.set_pagination(pagination)

        sort_fields = FilterMapper.parse_sort_string(self.sort)
        for sort_field in sort_fields:
            server_filter.add_sort(sort_field.field, sort_field.direction)

        return server_filter
