from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.infrastructure.db.models.base import BaseModelORM


class PaymentModel(BaseModelORM):
    __tablename__ = "payments"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    order_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)

    provider: Mapped[str] = mapped_column(String(64), nullable=False)

    status: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    external_id: Mapped[str | None] = mapped_column(String(256), nullable=True, unique=True)
    confirmation_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    idempotency_key: Mapped[str | None] = mapped_column(String(256), nullable=True, unique=True)
    provider_payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default="{}")

    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, server_default=func.now())
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
