from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import DomainEvent


@dataclass(frozen=True)
class VPNServerEnabledEvent(DomainEvent):
    __event_name__ = "vpn_server.enabled"

    server_id: UUID


@dataclass(frozen=True)
class VPNServerDisabledEvent(DomainEvent):
    __event_name__ = "vpn_server.disabled"

    server_id: UUID
