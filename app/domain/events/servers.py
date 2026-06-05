from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import DomainEvent
from app.domain.values.servers import PanelType


@dataclass(frozen=True)
class VPNServerActivatedEvent(DomainEvent):
    __event_name__ = "vpn_server.activated"
    server_id: UUID


@dataclass(frozen=True)
class VPNServerDeactivatedEvent(DomainEvent):
    __event_name__ = "vpn_server.deactivated"
    server_id: UUID


@dataclass(frozen=True)
class PanelConnectionCredentialsRotatedEvent(DomainEvent):
    __event_name__ = "panel_connection.credentials_rotated"
    panel_connection_id: UUID
    panel_type: PanelType

