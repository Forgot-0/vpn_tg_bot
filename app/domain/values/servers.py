from dataclasses import dataclass
from enum import Enum


class ProtocolType(Enum):
    vless = "VLESS"


class ApiType(Enum):
    x_ui = "3X-UI"


@dataclass(frozen=True)
class Region:
    flag: str
    name: str
    code: str
