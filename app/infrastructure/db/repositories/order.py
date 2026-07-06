from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.order import Order
from app.domain.repositories.orders import OrderRepository
from app.domain.values.order import OrderStatus, OrderType
from app.domain.values.money import Money
from app.infrastructure.db.mappers.order import OrderMapper
from app.infrastructure.db.models.order import OrderModel
from app.infrastructure.db.repositories.base import SQLAlchemyRepository


class SQLOrderRepository(SQLAlchemyRepository, OrderRepository):
    async def get_by_id(self, order_id: UUID) -> Order | None:
        result = await self.session.execute(select(OrderModel).where(OrderModel.id == order_id))
        order_model = result.scalar()
        return OrderMapper.from_order_model_to_domain(order_model) if order_model is not None else None

    async def list_by_user(self, user_id: UUID) -> list[Order]:
        result = await self.session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
        return [OrderMapper.from_order_model_to_domain(model) for model in result.scalars()]

    async def list_by_status(self, status: OrderStatus) -> list[Order]:
        result = await self.session.execute(select(OrderModel).where(OrderModel.status == status.value))
        return [OrderMapper.from_order_model_to_domain(model) for model in result.scalars()]

    async def add(self, order: Order) -> None:
        self.session.add(OrderMapper.from_order_domain_to_model(order))

    async def update(self, order: Order) -> None:
        await self.session.merge(OrderMapper.from_order_domain_to_model(order))
