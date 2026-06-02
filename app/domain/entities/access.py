from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.servers import PanelType
from app.domain.values.subscriptions import AccessCredential, ProvisioningStatus, RemoteAccessState


@dataclass
class ProvisionedAccess(AggregateRoot):
    id: UUID
    subscription_id: UUID
    server_id: UUID
    panel_type: PanelType
    panel_client_id: str
    inbound_ids: tuple[int, ...] = ()
    credentials: list[AccessCredential] = field(default_factory=list)
    status: ProvisioningStatus = ProvisioningStatus.PENDING
    remote_state: RemoteAccessState = RemoteAccessState.UNKNOWN
    used_traffic_gb: Decimal = Decimal("0")
    last_synced_at: datetime | None = None
    last_error: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.panel_client_id:
            raise ValueError("Provisioned access panel_client_id cannot be empty")
        if self.used_traffic_gb < 0:
            raise ValueError("Provisioned access used_traffic_gb cannot be negative")

    def mark_provisioning(self) -> None:
        self.status = ProvisioningStatus.PROVISIONING
        self.last_error = None

    def mark_active(self, credentials: list[AccessCredential]) -> None:
        self.credentials = credentials
        self.status = ProvisioningStatus.ACTIVE
        self.remote_state = RemoteAccessState.EXISTS
        self.last_error = None

    def mark_failed(self, reason: str) -> None:
        self.status = ProvisioningStatus.FAILED
        self.last_error = reason

    def suspend(self) -> None:
        self.status = ProvisioningStatus.SUSPENDED
        self.remote_state = RemoteAccessState.DISABLED

    def mark_deleted(self) -> None:
        self.status = ProvisioningStatus.DELETED
        self.remote_state = RemoteAccessState.DELETED

    def sync_usage(self, used_traffic_gb: Decimal, synced_at: datetime) -> Decimal:
        if used_traffic_gb < 0:
            raise ValueError("used_traffic_gb cannot be negative")
        delta = max(Decimal("0"), used_traffic_gb - self.used_traffic_gb)
        self.used_traffic_gb = used_traffic_gb
        self.last_synced_at = synced_at
        return delta
