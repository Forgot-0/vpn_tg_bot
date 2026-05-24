from app.domain.entities.payment import PaymentOrder
from app.domain.values.payments import PaymentProvider, PaymentStatus
from app.domain.values.subscriptions import Money
from app.infrastructure.db.models.payments import PaymentOrderModel


class PaymentMapper:
    @staticmethod
    def to_domain(model: PaymentOrderModel) -> PaymentOrder:
        return PaymentOrder(
            id=model.id,
            subscription_id=model.subscription_id,
            price=Money(amount=model.price_amount, currency=model.price_currency),
            provider=PaymentProvider(model.provider),
            status=PaymentStatus(model.status),
            external_payment_id=model.external_payment_id,
            confirmation_url=model.confirmation_url,
            created_at=model.created_at,
            paid_at=model.paid_at,
        )

    @staticmethod
    def to_model(entity: PaymentOrder) -> PaymentOrderModel:
        return PaymentOrderModel(
            id=entity.id,
            subscription_id=entity.subscription_id,
            price_amount=entity.price.amount,
            price_currency=entity.price.currency,
            provider=entity.provider.value,
            status=entity.status.value,
            external_payment_id=entity.external_payment_id,
            confirmation_url=entity.confirmation_url,
            created_at=entity.created_at,
            paid_at=entity.paid_at,
        )

    @staticmethod
    def update_model(model: PaymentOrderModel, entity: PaymentOrder) -> None:
        model.status = entity.status.value
        model.external_payment_id = entity.external_payment_id
        model.confirmation_url = entity.confirmation_url
        model.paid_at = entity.paid_at
