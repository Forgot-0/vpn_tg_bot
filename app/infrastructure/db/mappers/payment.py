from __future__ import annotations

from decimal import Decimal

from app.domain.entities.payment import Payment
from app.domain.values.money import Money
from app.domain.values.payments import PaymentProvider, PaymentStatus
from app.infrastructure.db.models.payment import PaymentModel


class PaymentMapper:
    @staticmethod
    def from_payment_domain_to_model(payment: Payment) -> PaymentModel:
        return PaymentModel(
            id=payment.id,
            order_id=payment.order_id,
            amount=payment.amount.amount,
            currency=payment.amount.currency,
            provider=payment.provider.value,
            status=payment.status.value,
            external_id=payment.external_id,
            confirmation_url=payment.confirmation_url,
            idempotency_key=payment.idempotency_key,
            provider_payload=payment.provider_payload,
            created_at=payment.created_at,
            paid_at=payment.paid_at,
        )

    @staticmethod
    def from_payment_model_to_domain(payment_model: PaymentModel) -> Payment:
        return Payment(
            id=payment_model.id,
            order_id=payment_model.order_id,
            amount=Money(amount=Decimal(str(payment_model.amount)), currency=payment_model.currency),
            provider=PaymentProvider(payment_model.provider),
            status=PaymentStatus(payment_model.status),
            external_id=payment_model.external_id,
            confirmation_url=payment_model.confirmation_url,
            idempotency_key=payment_model.idempotency_key,
            provider_payload=payment_model.provider_payload,
            created_at=payment_model.created_at,
            paid_at=payment_model.paid_at,
        )
