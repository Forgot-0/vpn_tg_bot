from decimal import Decimal

from app.domain.entities.payment import PaymentIntent
from app.domain.values.money import Money
from app.domain.values.payments import PaymentProvider, PaymentStatus
from app.infrastructure.db.models.payment_intents import PaymentIntentModel


class PaymentIntentMapper:
    @staticmethod
    def to_entity(model: PaymentIntentModel) -> PaymentIntent:
        return PaymentIntent(
            id=model.id,
            checkout_session_id=model.checkout_session_id,
            order_id=getattr(model, "order_id", None),
            user_id=model.user_id,
            amount=Money(Decimal(model.amount), model.currency),
            provider=PaymentProvider(model.provider),
            status=PaymentStatus(model.status),
            external_id=model.external_id,
            confirmation_url=model.confirmation_url,
            created_at=model.created_at,
            paid_at=model.paid_at,
            idempotency_key=getattr(model, "idempotency_key", None),
            provider_payload=getattr(model, "provider_payload", {}) or {},
        )

    @staticmethod
    def to_model(entity: PaymentIntent) -> PaymentIntentModel:
        return PaymentIntentModel(
            id=entity.id,
            checkout_session_id=entity.checkout_session_id,
            order_id=entity.order_id,
            user_id=entity.user_id,
            amount=entity.amount.amount,
            currency=entity.amount.currency,
            provider=entity.provider.value,
            status=entity.status.value,
            external_id=entity.external_id,
            confirmation_url=entity.confirmation_url,
            created_at=entity.created_at,
            paid_at=entity.paid_at,
            idempotency_key=entity.idempotency_key,
            provider_payload=entity.provider_payload,
        )

    @staticmethod
    def update_model(model: PaymentIntentModel, entity: PaymentIntent) -> None:
        model.order_id = entity.order_id
        model.checkout_session_id = entity.checkout_session_id
        model.amount = float(entity.amount.amount)
        model.currency = entity.amount.currency
        model.provider = entity.provider.value
        model.status = entity.status.value
        model.external_id = entity.external_id
        model.confirmation_url = entity.confirmation_url
        model.paid_at = entity.paid_at
        model.idempotency_key = entity.idempotency_key
        model.provider_payload = entity.provider_payload
