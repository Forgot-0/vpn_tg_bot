from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProtocolCode(StrEnum):
    SHADOWSOCKS = "shadowsocks"
    TROJAN = "trojan"
    VLESS = "vless"
    VMESS = "vmess"
    HYSTERIA2 = "hysteria2"
    TUIC = "tuic"
    WIREGUARD = "wireguard"


class FeatureCode(StrEnum):
    MULTI_HOP = "multi_hop"
    DEDICATED_IP = "dedicated_ip"
    STATIC_IP = "static_ip"
    HIGH_SPEED = "high_speed"
    EXTRA_PORTS = "extra_ports"
    OBFUSCATION = "obfuscation"


class PanelType(StrEnum):
    X3UI = "3x-ui"
    REMNAWAVE = "remnawave"
    MARZBAN = "marzban"
    OTHER = "other"


@dataclass(frozen=True)
class PanelCredentials:
    username: str
    password: str
    two_factor_secret: str | None = None


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
