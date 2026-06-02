from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.events.subscription_drafts import (
    SubscriptionDraftConvertedEvent,
    SubscriptionDraftExpiredEvent,
    SubscriptionDraftReadyForCheckoutEvent,
    SubscriptionDraftUpdatedEvent,
)
from app.domain.entities.subscription_plan import SubscriptionPlan
from app.domain.services.clock import now_utc
from app.domain.services.pricings import PricingService
from app.domain.values.money import Money
from app.domain.values.subscriptions import DraftStatus, SubscriptionSpec


@dataclass
class SubscriptionDraft(AggregateRoot):
    id: UUID
    user_id: UUID
    plan_id: UUID
    spec: SubscriptionSpec
    calculated_price: Money | None = None
    status: DraftStatus = DraftStatus.DRAFT
    server_id: UUID | None = None
    created_at: datetime = field(default_factory=now_utc)
    updated_at: datetime = field(default_factory=now_utc)


    def validate(self) -> None:
        if self.calculated_price is not None and self.calculated_price.amount <= 0:
            raise

    def update_spec(
        self,
        spec: SubscriptionSpec,
        plan: SubscriptionPlan,
        pricing_service: PricingService,
    ) -> None:
        self._require_mutable(action="update_spec")
        plan.validate_spec(spec)
        self.spec = spec
        self.recalculate_price(plan, pricing_service)
        self.updated_at = now_utc()
        self.register_event(
            SubscriptionDraftUpdatedEvent(
                draft_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id,
                status=self.status,
                calculated_price=self.calculated_price,
            )
        )

    def set_server(self, server_id: UUID) -> None:
        self._require_mutable(action="set_server")
        self.server_id = server_id
        self.updated_at = now_utc()
        self.register_event(
            SubscriptionDraftUpdatedEvent(
                draft_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id,
                status=self.status,
                calculated_price=self.calculated_price,
            )
        )

    def recalculate_price(
        self,
        plan: SubscriptionPlan,
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
        self._require_status({DraftStatus.DRAFT}, action="mark_ready_for_checkout")

        if self.server_id is None:
            raise

        if self.calculated_price is None:
            raise

        self.status = DraftStatus.READY_FOR_CHECKOUT
        self.updated_at = now_utc()
        self.register_event(
            SubscriptionDraftReadyForCheckoutEvent(
                draft_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id,
                calculated_price=self.calculated_price,
            )
        )

    def mark_converted(self, payment_order_id: UUID) -> None:
        self._require_status({DraftStatus.READY_FOR_CHECKOUT}, action="mark_converted")
        assert self.server_id is not None

        self.status = DraftStatus.CONVERTED
        self.updated_at = now_utc()
        self.register_event(
            SubscriptionDraftConvertedEvent(
                draft_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
                server_id=self.server_id,
                payment_order_id=payment_order_id,
            )
        )

    def expire(self) -> None:
        self._require_status({DraftStatus.DRAFT, DraftStatus.READY_FOR_CHECKOUT}, action="expire")
        self.status = DraftStatus.EXPIRED
        self.updated_at = now_utc()
        self.register_event(
            SubscriptionDraftExpiredEvent(
                draft_id=self.id,
                user_id=self.user_id,
                plan_id=self.plan_id,
            )
        )

    def _require_status(self, allowed: set[DraftStatus], *, action: str) -> None:
        if self.status not in allowed:
            raise

    def _require_mutable(self, *, action: str) -> None:
        if self.status in {DraftStatus.CONVERTED, DraftStatus.EXPIRED}:
            raise
