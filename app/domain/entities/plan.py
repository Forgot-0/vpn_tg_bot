from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.errors import SpecValidationError
from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import (
    PlanConfiguration,
    PlanOptionSet,
    PlanType,
    PlanVisibility,
    PricingRules,
    ProductType,
)


@dataclass
class Plan(AggregateRoot):
    id: UUID
    code: str
    name: str
    plan_type: PlanType

    product_id: UUID | None = None
    product_type: ProductType = ProductType.VPN_SUBSCRIPTION
    visibility: PlanVisibility = PlanVisibility.PUBLIC

    fixed_spec: PlanConfiguration | None = None
    fixed_price: Money | None = None

    constraints: PlanOptionSet | None = None
    pricing_rules: PricingRules | None = None

    allowed_region_codes: FrozenSet[str] = frozenset()
    allowed_location_ids: FrozenSet[UUID] = frozenset()
    allowed_server_group_ids: FrozenSet[UUID] = frozenset()

    description: str = ""
    is_active: bool = True
    is_public: bool = True
    sort_order: int = 0
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.is_public and self.visibility == PlanVisibility.HIDDEN:
            self.is_public = False
        if self.visibility == PlanVisibility.PRIVATE:
            self.is_public = False
        super().__post_init__()

    def validate(self) -> None:
        if not self.code:
            raise ValueError("Plan code cannot be empty")
        if not self.name:
            raise ValueError("Plan name cannot be empty")

        if self.plan_type == PlanType.FIXED:
            if self.fixed_spec is None:
                raise ValueError("FIXED plan requires fixed_spec")
            if self.fixed_price is None:
                raise ValueError("FIXED plan requires fixed_price")

        elif self.plan_type == PlanType.FLEXIBLE:
            if self.constraints is None:
                raise ValueError("FLEXIBLE plan requires constraints")
            if self.pricing_rules is None:
                raise ValueError("FLEXIBLE plan requires pricing_rules")

    @property
    def is_fixed(self) -> bool:
        return self.plan_type == PlanType.FIXED

    @property
    def is_flexible(self) -> bool:
        return self.plan_type == PlanType.FLEXIBLE

    def publish(self) -> None:
        self.is_public = True
        self.visibility = PlanVisibility.PUBLIC

    def hide(self) -> None:
        self.is_public = False
        self.visibility = PlanVisibility.HIDDEN

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def get_fixed_spec(self) -> PlanConfiguration:
        if not self.is_fixed or self.fixed_spec is None:
            raise
        return self.fixed_spec

    def get_fixed_price(self) -> Money:
        if not self.is_fixed or self.fixed_price is None:
            raise 
        return self.fixed_price

    def get_allowed_protocols(self) -> FrozenSet[ProtocolCode]:
        if self.is_fixed:
            return self.fixed_spec.protocols  # type: ignore[union-attr]
        return self.constraints.allowed_protocols  # type: ignore[union-attr]

    def get_allowed_features(self) -> FrozenSet[FeatureCode]:
        if self.is_fixed:
            return self.fixed_spec.features  # type: ignore[union-attr]
        return self.constraints.allowed_features  # type: ignore[union-attr]

    def validate_spec(self, spec: PlanConfiguration) -> None:
        if self.is_fixed:
            if spec != self.fixed_spec:
                raise
            return

        assert self.constraints is not None
        violations = self.constraints.check(spec)
        if violations:
            raise SpecValidationError(violations=violations)
