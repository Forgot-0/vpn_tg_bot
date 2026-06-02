from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import DomainEvent
from app.domain.values.money import Money
from app.domain.values.subscriptions import DraftStatus


@dataclass(frozen=True)
class SubscriptionDraftCreatedEvent(DomainEvent):
    __event_name__ = "subscription_draft.created"

    draft_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID | None
    status: DraftStatus
    calculated_price: Money | None


@dataclass(frozen=True)
class SubscriptionDraftUpdatedEvent(DomainEvent):
    __event_name__ = "subscription_draft.updated"

    draft_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID | None
    status: DraftStatus
    calculated_price: Money | None


@dataclass(frozen=True)
class SubscriptionDraftReadyForCheckoutEvent(DomainEvent):
    __event_name__ = "subscription_draft.ready_for_checkout"

    draft_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    calculated_price: Money


@dataclass(frozen=True)
class SubscriptionDraftConvertedEvent(DomainEvent):
    __event_name__ = "subscription_draft.converted"

    draft_id: UUID
    user_id: UUID
    plan_id: UUID
    server_id: UUID
    payment_order_id: UUID


@dataclass(frozen=True)
class SubscriptionDraftExpiredEvent(DomainEvent):
    __event_name__ = "subscription_draft.expired"

    draft_id: UUID
    user_id: UUID
    plan_id: UUID

