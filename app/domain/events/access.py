from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import DomainEvent
from app.domain.values.servers import PanelType


@dataclass(frozen=True)
class ProvisionedAccessCreatedEvent(DomainEvent):
    __event_name__ = "provisioned_access.created"

    access_id: UUID
    subscription_id: UUID
    server_id: UUID
    panel_type: PanelType
    panel_client_id: str
