
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import FrozenSet

from app.domain.values.servers import ProtocolCode
from app.domain.values.subscriptions import AccessCredential


@dataclass(frozen=True)
class CreateClientCommand:
    client_ref: str
    protocols: FrozenSet[ProtocolCode]
    traffic_limit_bytes: int | None
    expires_at: datetime | None
    max_devices: int
    label: str = ""


@dataclass(frozen=True)
class PanelClientResult:
    panel_client_id: str
    credentials: list[AccessCredential]


@dataclass(frozen=True)
class TrafficStats:
    used_bytes: int
    limit_bytes: int | None

    @property
    def used_gb(self) -> Decimal:
        return Decimal(str(self.used_bytes)) / Decimal("1073741824")  # 1024^3
