from uuid import UUID

from sqlalchemy import select

from app.domain.entities.payment import Payment
from app.domain.repositories.payments import PaymentRepository
from app.infrastructure.db.mappers.payment import PaymentMapper
from app.infrastructure.db.models.payment import PaymentModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLPaymentRepository(SQLAlchemyRepository, PaymentRepository):
    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        result = await self.session.execute(select(PaymentModel).where(PaymentModel.id == payment_id))
        payment_model = result.scalar()
        return PaymentMapper.from_payment_model_to_domain(payment_model) if payment_model is not None else None

    async def get_by_external_id(self, external_id: str) -> Payment | None:
        result = await self.session.execute(select(PaymentModel).where(PaymentModel.external_id == external_id))
        payment_model = result.scalar()
        return PaymentMapper.from_payment_model_to_domain(payment_model) if payment_model is not None else None

    async def get_by_order_id(self, order_id: UUID) -> Payment | None:
        result = await self.session.execute(select(PaymentModel).where(PaymentModel.order_id == order_id))
        payment_model = result.scalar()
        return PaymentMapper.from_payment_model_to_domain(payment_model) if payment_model is not None else None

    async def add(self, payment: Payment) -> None:
        self.session.add(PaymentMapper.from_payment_domain_to_model(payment))

    async def update(self, payment: Payment) -> None:
        await self.session.merge(PaymentMapper.from_payment_domain_to_model(payment))
