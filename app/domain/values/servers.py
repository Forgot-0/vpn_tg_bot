from dataclasses import dataclass
from enum import Enum


class ProtocolType(Enum):
    vless = "VLESS"
    mock = "MOCK"


class ApiType(Enum):
    x_ui = "3X-UI"
    mock = "MOCK"

@dataclass
class VPNConfig:
    protocol_type: ProtocolType
    config: str

@dataclass(frozen=True)
class Region:
    flag: str
    name: str
    code: str
