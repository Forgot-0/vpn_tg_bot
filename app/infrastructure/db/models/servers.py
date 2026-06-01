from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.models.base import BaseModelORM


class VPNServerModel(BaseModelORM):
    __tablename__ = "vpn_servers"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    region_code: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    panel_type: Mapped[str] = mapped_column(String(32), nullable=False)
    panel_host: Mapped[str] = mapped_column(String(255), nullable=False)
    panel_port: Mapped[int] = mapped_column(Integer, nullable=False)
    panel_path: Mapped[str] = mapped_column(String(255), nullable=False, default="/")
    panel_use_ssl: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    panel_username: Mapped[str | None] = mapped_column(String(128), nullable=True)
    panel_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    panel_two_factor_secret: Mapped[str | None] = mapped_column(String(255), nullable=True)
    panel_config: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)

    supported_protocols: Mapped[list] = mapped_column(ARRAY((String(128))), nullable=False, default=list)
    supported_features: Mapped[list] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    max_clients: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_clients: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    free: Mapped[int] = mapped_column(Integer, default=0)

    tags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
