from decimal import Decimal

from app.domain.entities.payment import PaymentOrder
from app.domain.values.money import Money
from app.domain.values.payments import PaymentProvider, PaymentStatus
from app.infrastructure.db.models.payments import PaymentOrderModel


class PaymentOrderMapper:
    @staticmethod
    def to_entity(model: PaymentOrderModel) -> PaymentOrder:
        return PaymentOrder(
            id=model.id,
            draft_id=model.draft_id,
            user_id=model.user_id,
            amount=Money(Decimal(model.amount), model.currency),
            provider=PaymentProvider(model.provider),
            status=PaymentStatus(model.status),
            external_id=model.external_id,
            confirmation_url=model.confirmation_url,
            created_at=model.created_at,
            paid_at=model.paid_at,
        )

    @staticmethod
    def to_model(entity: PaymentOrder) -> PaymentOrderModel:
        return PaymentOrderModel(
            id=entity.id,
            draft_id=entity.draft_id,
            user_id=entity.user_id,
            amount=entity.amount.amount,
            currency=entity.amount.currency,
            provider=entity.provider.value,
            status=entity.status.value,
            external_id=entity.external_id,
            confirmation_url=entity.confirmation_url,
            created_at=entity.created_at,
            paid_at=entity.paid_at,
        )

    @staticmethod
    def update_model(model: PaymentOrderModel, entity: PaymentOrder) -> None:
        model.amount = float(entity.amount.amount)
        model.currency = entity.amount.currency
        model.provider = entity.provider.value
        model.status = entity.status.value
        model.external_id = entity.external_id
        model.confirmation_url = entity.confirmation_url
        model.paid_at = entity.paid_at
