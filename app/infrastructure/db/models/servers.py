from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.models.base import BaseModelORM


class VPNServerModel(BaseModelORM):
    __tablename__ = "vpn_servers"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    region_code: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    panel_connection_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("panel_connections.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    location_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    server_group_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("server_groups.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    panel_config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    supported_protocols: Mapped[list] = mapped_column(
        ARRAY(String(128)), nullable=False, default=list
    )
    supported_features: Mapped[list] = mapped_column(
        ARRAY(String(128)), nullable=False, default=list
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    max_clients: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_clients: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    free: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=100)

    tags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)