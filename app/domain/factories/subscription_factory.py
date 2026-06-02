from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.domain.entities.payment import PaymentOrder
from app.domain.entities.subscription import Subscription
from app.domain.entities.subscription_draft import SubscriptionDraft
from app.domain.errors import InvalidStateTransitionError
from app.domain.values.subscriptions import DraftStatus, SubscriptionStatus


@dataclass(frozen=True)
class SubscriptionFactory:
    @staticmethod
    def from_draft(
        *,
        draft: SubscriptionDraft,
        payment_order: PaymentOrder,
    ) -> Subscription:
        if payment_order.draft_id != draft.id:
            raise

        if not payment_order.is_paid:
            raise

        if draft.status != DraftStatus.READY_FOR_CHECKOUT:
            raise

        if draft.server_id is None:
            raise

        return Subscription(
            id=uuid4(),
            user_id=draft.user_id,
            plan_id=draft.plan_id,
            server_id=draft.server_id,
            spec=draft.spec,
            status=SubscriptionStatus.PENDING_PAYMENT,
            payment_order_id=payment_order.id,
        )
