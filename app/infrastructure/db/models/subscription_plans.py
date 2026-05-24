from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.models.base import BaseModelORM


class SubscriptionPlanModel(BaseModelORM):
    __tablename__ = "subscription_plans"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    plan_type: Mapped[str] = mapped_column(String(16), nullable=False)
    fixed_spec: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    fixed_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    fixed_currency: Mapped[str | None] = mapped_column(String(8), nullable=True)
    constraints: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    pricing_rules: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
