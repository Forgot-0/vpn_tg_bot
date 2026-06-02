from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.domain.entities.payment import PaymentIntent
from app.domain.entities.subscription import Subscription
from app.domain.entities.checkout import CheckoutSession
from app.domain.errors import BusinessRuleViolationError
from app.domain.values.subscriptions import CheckoutStatus


@dataclass(frozen=True)
class SubscriptionFactory:
    @staticmethod
    def from_checkout(
        *,
        checkout: CheckoutSession,
        payment_intent: PaymentIntent,
    ) -> Subscription:
        if payment_intent.checkout_session_id != checkout.id and payment_intent.order_id != checkout.order_id:
            raise BusinessRuleViolationError(reason="Payment intent does not belong to checkout session")

        if not payment_intent.is_paid:
            raise BusinessRuleViolationError(reason="Payment intent must be paid before subscription creation")

        if checkout.status not in {CheckoutStatus.READY_FOR_CHECKOUT, CheckoutStatus.READY_FOR_PAYMENT}:
            raise BusinessRuleViolationError(reason="Checkout session is not ready for conversion")

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
