from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ProtocolCode(StrEnum):
    SUBSCRIPTION = "subs"
    SHADOWSOCKS = "shadowsocks"
    TROJAN = "trojan"
    VLESS = "vless"
    VMESS = "vmess"
    HYSTERIA2 = "hysteria2"
    TUIC = "tuic"
    WIREGUARD = "wireguard"


class FeatureCode(StrEnum):
    WHITE_LIST = "white_list"
    DEDICATED_IP = "dedicated_ip"
    GEO_ROUTING = "geo_routing"
    XRAY_ROUTING = "xray_routing"
    ANTI_DPI = "anti_dpi"
    GAMING_MODE = "gaming_mode"
    PRIORITY_TRAFFIC = "priority_traffic"
    MULTI_HOP = "multi_hop"
    OBFUSCATION = "obfuscation"
    HIGH_SPEED = "high_speed"


class PanelType(StrEnum):
    X3UI = "3x-ui"
    REMNAWAVE = "remnawave"
    MARZBAN = "marzban"
    OTHER = "other"


@dataclass(frozen=True)
class PanelCredentials:
    username: str | None = None
    password: str | None = None
    api_token: str | None = None

    def __post_init__(self) -> None:
        if self.username is None and self.api_token is None:
            raise

        if self.username is not None and self.password is None:
            raise


@dataclass(frozen=True)
class PanelEndpoint:
    host: str
    port: int
    path: str = "/"
    use_ssl: bool = True

    @property
    def base_url(self) -> str:
        scheme = "https" if self.use_ssl else "http"
        path = self.path.lstrip("/")
        return f"{scheme}://{self.host}:{self.port}/{path}"


@dataclass(frozen=True)
class Capacity:
    max_client: int = field(default=0)
    free: int = field(default=0)

    @property
    def available_slots(self) -> int:
        return max(0, self.max_client - self.free)

    @property
    def load_percent(self) -> float:
        if self.max_client == 0:
            return 100.0
        return (self.free / self.max_client) * 100

    @property
    def has_capacity(self) -> bool:
        return self.available_slots > 0


@dataclass(frozen=True)
class Location:
    code: str
    name: str
    flag: str = ""

    @classmethod
    def get_from_code(cls, code: str) -> Location:
        return cls(
            code=code,
            name="",
            flag=""
        )
