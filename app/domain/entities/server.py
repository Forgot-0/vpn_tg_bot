from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, FrozenSet
from uuid import UUID

from app.domain.entities.base import AggregateRoot
from app.domain.values.servers import FeatureCode, PanelCredentials, PanelEndpoint, PanelType, ProtocolCode
from app.domain.values.subscriptions import PlanConfiguration


@dataclass(frozen=True)
class CapacityPolicy:
    max_clients: int | None = None
    max_traffic_gb: Decimal | None = None
    weight: int = 100

    def __post_init__(self) -> None:
        if self.max_clients is not None and self.max_clients < 0:
            raise ValueError("max_clients cannot be negative")
        if self.max_traffic_gb is not None and self.max_traffic_gb <= 0:
            raise ValueError("max_traffic_gb must be positive")
        if self.weight < 0:
            raise ValueError("weight cannot be negative")


@dataclass
class Location(AggregateRoot):
    id: UUID
    country_code: str
    title: str
    city: str | None = None
    emoji: str = ""
    is_public: bool = True
    sort_order: int = 0
    metadata: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.country_code:
            raise ValueError("Location country_code cannot be empty")
        if not self.title:
            raise ValueError("Location title cannot be empty")


@dataclass
class PanelConnection(AggregateRoot):
    id: UUID
    panel_type: PanelType
    endpoint: PanelEndpoint
    credentials: PanelCredentials
    config: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True

    def validate(self) -> None:
        if not self.endpoint.host:
            raise ValueError("Panel connection host cannot be empty")


@dataclass
class ServerGroup(AggregateRoot):
    id: UUID
    name: str
    location_id: UUID | None = None
    capacity_policy: CapacityPolicy = field(default_factory=CapacityPolicy)
    is_active: bool = True
    is_public: bool = True
    sort_order: int = 0
    tags: FrozenSet[str] = frozenset()

    def validate(self) -> None:
        if not self.name:
            raise ValueError("ServerGroup name cannot be empty")


@dataclass
class Inbound(AggregateRoot):
    id: UUID
    server_id: UUID
    panel_inbound_id: int
    protocol: ProtocolCode
    features: FrozenSet[FeatureCode] = frozenset()
    is_active: bool = True
    config: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.panel_inbound_id < 0:
            raise ValueError("panel_inbound_id cannot be negative")


@dataclass
class VPNServer(AggregateRoot):
    id: UUID
    name: str
    region_code: str

    panel_type: PanelType
    panel_endpoint: PanelEndpoint
    panel_credentials: PanelCredentials

    location_id: UUID | None = None
    server_group_id: UUID | None = None
    panel_connection_id: UUID | None = None
    capacity_policy: CapacityPolicy = field(default_factory=CapacityPolicy)

    supported_protocols: FrozenSet[ProtocolCode] = frozenset()
    supported_features: FrozenSet[FeatureCode] = frozenset()

    is_active: bool = True

    max_clients: int | None = None
    current_clients: int = 0
    used_traffic_gb: Decimal = Decimal("0")

    tags: FrozenSet[str] = frozenset()
    panel_config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_clients is None and self.capacity_policy.max_clients is not None:
            self.max_clients = self.capacity_policy.max_clients
        if self.capacity_policy.max_clients is None and self.max_clients is not None:
            self.capacity_policy = CapacityPolicy(
                max_clients=self.max_clients,
                max_traffic_gb=self.capacity_policy.max_traffic_gb,
                weight=self.capacity_policy.weight,
            )
        super().__post_init__()

    def validate(self) -> None:
        if not self.name:
            raise ValueError("VPNServer name cannot be empty")
        if not self.region_code:
            raise ValueError("VPNServer region_code cannot be empty")
        if self.current_clients < 0:
            raise ValueError("current_clients cannot be negative")

    def can_accommodate(self, spec: PlanConfiguration) -> bool:
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
    def free_clients(self) -> int | None:
        if self.max_clients is None:
            return None
        return max(0, self.max_clients - self.current_clients)

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
        if self.max_clients is not None and self.current_clients >= self.max_clients:
            raise ValueError("Server capacity exceeded")
        self.current_clients += 1

    def decrement_clients(self) -> None:
        if self.current_clients > 0:
            self.current_clients -= 1
