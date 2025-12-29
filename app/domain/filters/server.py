from dataclasses import dataclass

from app.domain.filters.base import BaseFilter
from app.domain.filters.operators import FilterOperator


@dataclass
class ServerFilter(BaseFilter):
    region_code: str| None = None
    api_type: str| None = None
    min_free_slots: int| None = None
    max_free_slots: int| None = None
    protocol_types: list[str]| None = None
    has_domain: bool| None = None

    def __post_init__(self):
        self._build_conditions()

    def _build_conditions(self) -> None:
        self.add_condition("region.code", FilterOperator.EQ, self.region_code)
        self.add_condition("api_type", FilterOperator.EQ, self.api_type)

        if self.min_free_slots is not None:
            self.add_condition("free", FilterOperator.GTE, self.min_free_slots)

        if self.max_free_slots is not None:
            self.add_condition("free", FilterOperator.LTE, self.max_free_slots)

        if self.has_domain is not None:
            operator = FilterOperator.NE if self.has_domain else FilterOperator.EQ
            self.add_condition("api_config.domain", operator, None)

