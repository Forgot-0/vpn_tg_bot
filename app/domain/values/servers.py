from dataclasses import dataclass
from enum import StrEnum


class PanelType(StrEnum):
    X3UI = "3x-ui"
    REMNAWAVE = "remnawave"
    MARBZAN = "marbzan"
    OTHER = "other"


class ProtocolCode(StrEnum):
    SHADOWSOCKS = "shadowsocks"
    TROJAN = "trojan"
    HYSTERIA2 = "hysteria2"
    TUIC = "tuic"
    WIREGUARD = "wireguard"


@dataclass(frozen=True)
class PanelCredentials:
    username: str
    password: str
    two_factor_code: str | None = None


@dataclass(frozen=True)
class PanelConfig:
    host: str
    panel_port: int
    panel_path: str
    domain: str | None = None
