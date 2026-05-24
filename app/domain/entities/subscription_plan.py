from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.errors import BusinessRuleViolationError, SpecValidationError
from app.domain.values.money import Money
from app.domain.values.servers import FeatureCode, ProtocolCode
from app.domain.values.subscriptions import (
    PlanConstraints,
    PlanType,
    PricingRules,
    SubscriptionSpec,
)


@dataclass
class SubscriptionPlan(AggregateRoot):
    id: UUID
    code: str
    name: str
    plan_type: PlanType

    fixed_spec: SubscriptionSpec | None = None
    fixed_price: Money | None = None

    constraints: PlanConstraints | None = None
    pricing_rules: PricingRules | None = None

    description: str = ""
    is_active: bool = True
    is_public: bool = True
    sort_order: int = 0

    def _validate(self) -> None:
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

    def get_fixed_spec(self) -> SubscriptionSpec:
        if not self.is_fixed or self.fixed_spec is None:
            raise BusinessRuleViolationError(reason="Plan is not FIXED")
        return self.fixed_spec

    def get_fixed_price(self) -> Money:
        if not self.is_fixed or self.fixed_price is None:
            raise BusinessRuleViolationError(reason="Plan is not FIXED")
        return self.fixed_price

    def get_allowed_protocols(self) -> FrozenSet[ProtocolCode]:
        if self.is_fixed:
            return self.fixed_spec.protocols  # type: ignore[union-attr]
        return self.constraints.allowed_protocols  # type: ignore[union-attr]

    def get_allowed_features(self) -> FrozenSet[FeatureCode]:
        if self.is_fixed:
            return self.fixed_spec.features # type: ignore[union-attr]
        return self.constraints.allowed_features  # type: ignore[union-attr]

    def validate_spec(self, spec: SubscriptionSpec) -> None:
        if self.is_fixed:
            if spec != self.fixed_spec:
                raise BusinessRuleViolationError(
                    reason="Spec does not match the fixed plan configuration"
                )
            return

        assert self.constraints is not None
        violations = self.constraints.check(spec)
        if violations:
            raise SpecValidationError(violations=violations)
