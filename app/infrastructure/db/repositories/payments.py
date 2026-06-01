from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.payment import PaymentOrder
from app.domain.repositories.payments import PaymentOrderRepository
from app.domain.values.payments import PaymentStatus
from app.infrastructure.db.mappers.payments import PaymentOrderMapper
from app.infrastructure.db.models.payments import PaymentOrderModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


@dataclass
class SQLAlchemyPaymentOrderRepository(SQLAlchemyRepository, PaymentOrderRepository):
    async def get_by_id(self, payment_id: UUID) -> PaymentOrder | None:
        model = await self.session.get(PaymentOrderModel, payment_id)
        return PaymentOrderMapper.to_entity(model) if model else None

    async def get_by_external_id(self, external_id: str) -> PaymentOrder | None:
        stmt = select(PaymentOrderModel).where(PaymentOrderModel.external_id == external_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PaymentOrderMapper.to_entity(model) if model else None

    async def get_pending_for_subscription(self, subscription_id: UUID) -> PaymentOrder | None:
        stmt = (
            select(PaymentOrderModel)
            .where(PaymentOrderModel.subscription_id == subscription_id)
            .where(
                PaymentOrderModel.status.in_(
                    [PaymentStatus.PENDING.value, PaymentStatus.WAITING_FOR_CAPTURE.value]
                )
            )
            .order_by(PaymentOrderModel.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PaymentOrderMapper.to_entity(model) if model else None

    async def add(self, payment: PaymentOrder) -> None:
        self.session.add(PaymentOrderMapper.to_model(payment))

    async def update(self, payment: PaymentOrder) -> None:
        model = await self.session.get(PaymentOrderModel, payment.id)
        if model is None:
            raise LookupError(f"PaymentOrder {payment.id} not found")
        PaymentOrderMapper.update_model(model, payment)
