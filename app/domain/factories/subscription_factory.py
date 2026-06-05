from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.domain.entities.payment import PaymentIntent
from app.domain.entities.subscription import Subscription
from app.domain.entities.checkout import CheckoutSession
from app.domain.values.subscriptions import CheckoutStatus


@dataclass(frozen=True)
class SubscriptionFactory:

    @staticmethod
    def from_checkout(
        *,
        checkout: CheckoutSession,
        payment_intent: PaymentIntent,
    ) -> Subscription:
        belongs_to_checkout = (
            payment_intent.checkout_session_id == checkout.id
            or payment_intent.order_id == checkout.order_id
        )
        if not belongs_to_checkout:
            raise

        if not payment_intent.is_paid:
            raise

        return Subscription.pending_provisioning(
            id=uuid4(),
            user_id=checkout.user_id,
            plan_id=checkout.plan_id,
            server_id=checkout.server_id,
            spec=checkout.spec,
            order_id=checkout.order_id,
            payment_intent_id=payment_intent.id,
            purchased_price=payment_intent.amount,
        )
