from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.payment import PaymentIntent
from app.domain.repositories.payments import PaymentIntentRepository
from app.domain.values.payments import PaymentStatus
from app.infrastructure.db.mappers.payment_intents import PaymentIntentMapper
from app.infrastructure.db.models.payment_intents import PaymentIntentModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemyPaymentIntentRepository(SQLAlchemyRepository, PaymentIntentRepository):
    async def get_by_id(self, payment_id: UUID) -> PaymentIntent | None:
        model = await self.session.get(PaymentIntentModel, payment_id)
        return PaymentIntentMapper.to_entity(model) if model else None

    async def get_by_external_id(self, external_id: str) -> PaymentIntent | None:
        stmt = select(PaymentIntentModel).where(PaymentIntentModel.external_id == external_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PaymentIntentMapper.to_entity(model) if model else None

    async def get_pending_for_checkout(self, checkout_session_id: UUID) -> PaymentIntent | None:
        stmt = (
            select(PaymentIntentModel)
            .where(PaymentIntentModel.checkout_session_id == checkout_session_id)
            .where(
                PaymentIntentModel.status.in_(
                    [PaymentStatus.PENDING.value, PaymentStatus.WAITING_FOR_CAPTURE.value]
                )
            )
            .order_by(PaymentIntentModel.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PaymentIntentMapper.to_entity(model) if model else None

    async def add(self, payment: PaymentIntent) -> None:
        self.session.add(PaymentIntentMapper.to_model(payment))

    async def update(self, payment: PaymentIntent) -> None:
        model = await self.session.get(PaymentIntentModel, payment.id)
        if model is None:
            raise LookupError(f"PaymentIntent {payment.id} not found")
        PaymentIntentMapper.update_model(model, payment)
