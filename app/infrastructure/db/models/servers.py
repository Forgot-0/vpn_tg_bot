from typing import Any
from uuid import UUID

from sqlalchemy import UUID as SAUUID, Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.models.base import BaseModelORM



class VPNServerModel(BaseModelORM):
    __tablename__ = "vpn_servers"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True)

    panel_type: Mapped[str] = mapped_column(String(32), nullable=False)
    panel_ip: Mapped[str] = mapped_column(String(64), nullable=False)
    panel_port: Mapped[int] = mapped_column(Integer, nullable=False)
    panel_path: Mapped[str] = mapped_column(String(256), nullable=False)
    panel_domain: Mapped[str | None] = mapped_column(String(256), nullable=True)

    panel_username: Mapped[str] = mapped_column(String(256), nullable=False)
    panel_password: Mapped[str] = mapped_column(Text, nullable=False)
    panel_two_factor_code: Mapped[str | None] = mapped_column(String(64), nullable=True)

    region_code: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    supported_protocols: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    supported_features: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    protocols_config: Mapped[dict[str, dict[str, Any]]] = mapped_column(
        JSONB, nullable=False, default="{}"
    )

