from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID

from app.application.dtos.base import BaseDTO
from app.domain.entities.base import AggregateRoot
from app.domain.entities.server import VPNServer


@dataclass
class AddServerResultDTO(BaseDTO):
    server_id: UUID
    name: str
    region_code: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            server_id=data["server_id"],
            name=data["name"],
            region_code=data["region_code"],
        )

    @classmethod
    def from_entity(cls, entity: AggregateRoot) -> Self:
        if not isinstance(entity, VPNServer):
            raise TypeError(f"Expected VPNServer, got {type(entity).__name__}")
        return cls(
            server_id=entity.id,
            name=entity.name,
            region_code=entity.region_code,
        )
