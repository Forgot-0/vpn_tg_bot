from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.entities.plan import Plan
from app.domain.errors import BusinessRuleViolationError, InvalidStateTransitionError
from app.domain.events.checkout_sessions import (
    CheckoutSessionConvertedEvent,
    CheckoutSessionExpiredEvent,
    CheckoutSessionReadyForCheckoutEvent,
    CheckoutSessionUpdatedEvent,
)
from app.domain.services.clock import now_utc
from app.domain.services.pricings import PricingService
from app.domain.values.money import Money
from app.domain.values.subscriptions import CheckoutStatus, PlanConfiguration


@dataclass
class CheckoutSession(AggregateRoot):
    id: UUID
    user_id: UUID
    plan_id: UUID
    spec: PlanConfiguration
    calculated_price: Money | None = None
    status: CheckoutStatus = CheckoutStatus.DRAFT
    server_id: UUID | None = None
    offer_id: UUID | None = None
    price_id: UUID | None = None
    order_id: UUID | None = None
    expires_at: datetime | None = None
    metadata: dict[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=now_utc)
    updated_at: datetime = field(default_factory=now_utc)

    def validate(self) -> None:
        if self.calculated_price is not None and self.calculated_price.amount <= 0:
            raise ValueError("Checkout calculated price must be positive")

    def update_spec(
        self,
        spec: PlanConfiguration,
        plan: Plan,
        pricing_service: PricingService,
    ) -> None:
        self._require_mutable(action="update_spec")
        plan.validate_spec(spec)
        self.spec = spec
        self.recalculate_price(plan, pricing_service)
        self.updated_at = now_utc()
        self._register_updated()

    def set_server(self, server_id: UUID) -> None:
        self._require_mutable(action="set_server")
        self.server_id = server_id
        self.updated_at = now_utc()
        self._register_updated()

    def attach_offer(self, *, offer_id: UUID | None, price_id: UUID | None) -> None:
        self._require_mutable(action="attach_offer")
        self.offer_id = offer_id
        self.price_id = price_id
        self.updated_at = now_utc()
        self._register_updated()

    def recalculate_price(
        self,
        plan: Plan,
        pricing_service: PricingService,
    ) -> None:
        self._require_mutable(action="recalculate_price")
        if plan.is_fixed:
            self.calculated_price = plan.get_fixed_price()
        else:
            assert plan.pricing_rules is not None
            self.calculated_price = pricing_service.calculate(self.spec, plan.pricing_rules)
        self.updated_at = now_utc()

    def mark_ready_for_checkout(self) -> None:
        self._require_status({CheckoutStatus.DRAFT, CheckoutStatus.OPEN}, action="mark_ready_for_checkout")
        if self.server_id is None:
            raise BusinessRuleViolationError(reason="Checkout session requires a selected server")
        if self.calculated_price is None:
            raise BusinessRuleViolationError(reason="Checkout session requires calculated price")

        self.status = CheckoutStatus.READY_FOR_CHECKOUT
        self.updated_at = now_utc()
        self.register_event(
            CheckoutSessionReadyForCheckoutEvent(
                checkout_session_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id,
                calculated_price=self.calculated_price,
            )
        )

    def attach_order(self, order_id: UUID) -> None:
        self._require_status({CheckoutStatus.READY_FOR_CHECKOUT, CheckoutStatus.READY_FOR_PAYMENT}, action="attach_order")
        self.order_id = order_id
        self.status = CheckoutStatus.READY_FOR_PAYMENT
        self.updated_at = now_utc()

    def mark_converted(self, payment_intent_id: UUID) -> None:
        self._require_status({CheckoutStatus.READY_FOR_CHECKOUT, CheckoutStatus.READY_FOR_PAYMENT}, action="mark_converted")
        if self.server_id is None:
            raise BusinessRuleViolationError(reason="Checkout session requires a selected server")

        self.status = CheckoutStatus.CONVERTED
        self.updated_at = now_utc()
        self.register_event(
            CheckoutSessionConvertedEvent(
                checkout_session_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id,
                payment_intent_id=payment_intent_id,
            )
        )

    def expire(self) -> None:
        self._require_status(
            {CheckoutStatus.DRAFT, CheckoutStatus.OPEN, CheckoutStatus.READY_FOR_CHECKOUT, CheckoutStatus.READY_FOR_PAYMENT},
            action="expire",
        )
        self.status = CheckoutStatus.EXPIRED
        self.updated_at = now_utc()
        self.register_event(
            CheckoutSessionExpiredEvent(
                checkout_session_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
            )
        )

    def _register_updated(self) -> None:
        self.register_event(
            CheckoutSessionUpdatedEvent(
                checkout_session_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id,
                status=self.status,
                calculated_price=self.calculated_price,
            )
        )

    def _require_status(self, allowed: set[CheckoutStatus], *, action: str) -> None:
        if self.status not in allowed:
            raise InvalidStateTransitionError(reason=f"Cannot {action} checkout session in status {self.status}")

    def _require_mutable(self, *, action: str) -> None:
        if self.status in {CheckoutStatus.CONVERTED, CheckoutStatus.COMPLETED, CheckoutStatus.EXPIRED, CheckoutStatus.CANCELLED}:
            raise InvalidStateTransitionError(reason=f"Cannot {action} checkout session in status {self.status}")
