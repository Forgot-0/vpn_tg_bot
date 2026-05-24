from uuid import UUID

from sqlalchemy import select

from app.domain.entities.payment import PaymentOrder
from app.domain.repositories.payments import PaymentOrderRepository
from app.infrastructure.db.mappers.payments import PaymentMapper
from app.infrastructure.db.models.payments import PaymentOrderModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLAlchemyPaymentOrderRepository(
    SQLAlchemyRepository,
    PaymentOrderRepository,
):
    async def get_by_id(self, payment_id: UUID) -> PaymentOrder | None:
        query = select(PaymentOrderModel).where(PaymentOrderModel.id == payment_id)
        payment = (await self.session.execute(query)).scalar()
        return PaymentMapper.to_domain(payment) if payment else None

    async def get_by_subscription_id(self, subscription_id: UUID) -> PaymentOrder | None:
        query = select(PaymentOrderModel).where(
            PaymentOrderModel.subscription_id == subscription_id
        )
        payment = (await self.session.execute(query)).scalar()
        return PaymentMapper.to_domain(payment) if payment else None

    async def add(self, payment: PaymentOrder) -> None:
        self.session.add(PaymentMapper.to_model(payment))

    async def update(self, payment: PaymentOrder) -> None:
        query = select(PaymentOrderModel).where(PaymentOrderModel.id == payment.id)
        payment_model = (await self.session.execute(query)).scalar_one_or_none()
        if payment_model is None:
            raise ValueError(f"PaymentOrder {payment.id} not found")
        PaymentMapper.update_model(payment_model, payment)
