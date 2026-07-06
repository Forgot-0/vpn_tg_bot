from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, Enum, Integer, String, DECIMAL
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.values.subscriptions import PlanVisibility, TrafficResetStrategy
from app.infrastructure.db.models.base import BaseModelORM


class SubscriptionPlanModel(BaseModelORM):
    __tablename__ = "subscription_plans"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)

    code: Mapped[str] = mapped_column(String(256), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)

    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    traffic_limit_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_devices: Mapped[int | None] = mapped_column(Integer, nullable=True)

    features: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    protocols: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)

    strategy: Mapped[TrafficResetStrategy] = mapped_column(Enum(TrafficResetStrategy), nullable=False)
    reset_every_n_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    custom_cron: Mapped[str | None] = mapped_column(String(128), nullable=True)

    price: Mapped[list[dict[str, str]]] = mapped_column(JSONB, nullable=False, default=list)
    price_rule: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)

    visibility: Mapped[PlanVisibility] = mapped_column(Enum(PlanVisibility), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    is_trial: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    allowed_durations: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False, default=list)
    allowed_traffic_gb: Mapped[list[DECIMAL]] = mapped_column(ARRAY(DECIMAL), nullable=False, default=list)
    max_devices_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    allowed_features: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    allowed_protocols: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)

    server_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

