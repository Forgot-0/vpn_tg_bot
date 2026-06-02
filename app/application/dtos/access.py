from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.application.dtos.subscriptions import AccessCredentialDTO
from app.domain.entities.access import ProvisionedAccess


@dataclass
class ProvisionedAccessDTO(BaseDTO):
    id: UUID
    subscription_id: UUID
    server_id: UUID
    panel_type: str
    panel_client_id: str
    inbound_ids: tuple[int, ...]
    credentials: list[AccessCredentialDTO]
    status: str
    remote_state: str
    used_traffic_gb: Decimal
    last_error: str | None

    @classmethod
    def from_entity(cls, entity: ProvisionedAccess) -> Self:
        return cls(
            id=entity.id,
            subscription_id=entity.subscription_id,
            server_id=entity.server_id,
            panel_type=entity.panel_type.value,
            panel_client_id=entity.panel_client_id,
            inbound_ids=entity.inbound_ids,
            credentials=[AccessCredentialDTO.from_entity(item) for item in entity.credentials],
            status=entity.status.value,
            remote_state=entity.remote_state.value,
            used_traffic_gb=entity.used_traffic_gb,
            last_error=entity.last_error,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
