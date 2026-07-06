from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from app.infrastructure.db.models.base import BaseModelORM



class VPNServerModel(BaseModelORM):
    __tablename__ = "vpn_servers"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)

    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    max_client: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    free: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    panel_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    panel_host: Mapped[str] = mapped_column(String(512), nullable=False)
    panel_port: Mapped[int] = mapped_column(Integer, nullable=False)
    panel_path: Mapped[str] = mapped_column(String(512), nullable=False, default="/")
    panel_use_ssl: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    panel_username: Mapped[str | None] = mapped_column(String(256), nullable=True)
    panel_password: Mapped[str | None] = mapped_column(String(512), nullable=True)
    panel_api_token: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    locations: Mapped[dict[str, str]] = mapped_column(JSONB, nullable=False, default="{}")
    support_protocols: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default="[]")
    support_features: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default="[]")

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default="[]")
