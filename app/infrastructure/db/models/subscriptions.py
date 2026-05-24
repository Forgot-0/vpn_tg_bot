from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    UUID as SAUUID,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.base import BaseModelORM


class SubscriptionPlanModel(BaseModelORM):
    __tablename__ = "subscription_plans"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    billing_mode: Mapped[str] = mapped_column(String(32), nullable=False)

    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    traffic_quota_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_devices: Mapped[int | None] = mapped_column(Integer, nullable=True)

    allowed_protocols: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    included_features: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)

    fixed_price_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    fixed_price_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class SubscriptionModel(BaseModelORM):
    __tablename__ = "subscriptions"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    plan_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True),
        ForeignKey("subscription_plans.id", ondelete="RESTRICT"),
        nullable=False,
    )
    server_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True),
        ForeignKey("vpn_servers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    payment_order_id: Mapped[UUID | None] = mapped_column(
        SAUUID(as_uuid=True),
        ForeignKey(
            "payments.id",
            ondelete="SET NULL",
            use_alter=True,
            name="fk_subscriptions_payment_order_id",
        ),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", index=True)

    started_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    expires_at: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)

    purchased_price_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    purchased_price_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")

    used_traffic_gb: Mapped[Decimal] = mapped_column(
        Numeric(20, 6), nullable=False, default=Decimal("0")
    )

    access_items: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)


