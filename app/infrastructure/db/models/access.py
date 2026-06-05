from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.models.base import BaseModelORM


class ProvisionedAccessModel(BaseModelORM):
    __tablename__ = "provisioned_accesses"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    subscription_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    server_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("vpn_servers.id", ondelete="RESTRICT"), nullable=False, index=True)
    panel_type: Mapped[str] = mapped_column(String(32), nullable=False)
    panel_client_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    inbound_ids: Mapped[list] = mapped_column(ARRAY(String(32)), nullable=False, default=list)
    credentials: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    remote_state: Mapped[str] = mapped_column(String(32), nullable=False)
    used_traffic_gb: Mapped[float] = mapped_column(Numeric(16, 4), nullable=False, default=0)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
