from dataclasses import dataclass
from enum import Enum


class ProtocolType(Enum):
    vless = "VLESS"


class ApiType(Enum):
    x_ui = "3X-UI"

@dataclass
class VPNConfig:
    protocol_type: ProtocolType
    config: str

@dataclass(frozen=True)
class Region:
    flag: str
    name: str
    code: str
