from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.servers import (
    FeatureCode,
    PanelCredentials,
    PanelEndpoint,
    PanelType,
    ProtocolCode,
)
from app.domain.values.subscriptions import SubscriptionSpec


@dataclass
class VPNServer(AggregateRoot):
    id: UUID
    name: str
    region_code: str

    panel_type: PanelType
    panel_endpoint: PanelEndpoint
    panel_credentials: PanelCredentials

    supported_protocols: FrozenSet[ProtocolCode] = frozenset()
    supported_features: FrozenSet[FeatureCode] = frozenset()

    is_active: bool = True

    max_clients: int | None = None
    current_clients: int = 0

    tags: FrozenSet[str] = frozenset()

    def validate(self) -> None:
        if not self.name:
            raise ValueError("VPNServer name cannot be empty")
        if not self.region_code:
            raise ValueError("VPNServer region_code cannot be empty")

    def can_accommodate(self, spec: SubscriptionSpec) -> bool:
        if not self.is_active:
            return False
        if not spec.protocols.issubset(self.supported_protocols):
            return False
        if not spec.features.issubset(self.supported_features):
            return False
        if self.max_clients is not None and self.current_clients >= self.max_clients:
            return False
        return True

    def supports_protocol(self, protocol: ProtocolCode) -> bool:
        return protocol in self.supported_protocols

    def supports_feature(self, feature: FeatureCode) -> bool:
        return feature in self.supported_features

    @property
    def load_ratio(self) -> float | None:
        if self.max_clients is None:
            return None
        if self.max_clients == 0:
            return 1.0
        return self.current_clients / self.max_clients

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def increment_clients(self) -> None:
        self.current_clients += 1

    def decrement_clients(self) -> None:
        self.current_clients = max(0, self.current_clients - 1)
