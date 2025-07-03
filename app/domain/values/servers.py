from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CountryCode(Enum):
    RUSSIA = 'RU'
    VIETNAM = 'VN'
    THAILAND = 'TH'
    PHILIPPINES = 'PH'
    MALAYSIA = 'MY'
    SINGAPORE = 'SG'
    JAPAN = 'JP'
    SOUTH_KOREA = 'KR'
    HONG_KONG = 'HK'
    TAIWAN = 'TW'
    INDIA = 'IN'
    INDONESIA = 'ID'
    AMERICA = 'USA'
    GERMANY = 'DE'
    FRANCE = "FR"
    POLAND = "PL"
    ITALY = "IT"
    CANADA = "CA"
    BRAZIL = "BR"
    AUSTRALIA = "AU"
    SWITZERLAND = "CH"


class ProtocolType(Enum):
    vless = "VLESS"
    mock = "MOCK"

@dataclass(frozen=True)
class ProtocolConfig:
    config: dict[str, Any]
    protocol_type: ProtocolType


class ApiType(Enum):
    x_ui = "3X-UI"
    mock = "MOCK"

@dataclass(frozen=True)
class Base_APIConfig:
    ...

@dataclass(frozen=True)
class XUI_APIConfig(Base_APIConfig):
    ip: str
    panel_port: int
    panel_path: str

    domain: str | None = field(default=None)


@dataclass(frozen=True)
class Mock_APIConfig(Base_APIConfig):
    dummy_data: str


@dataclass
class VPNConfig:
    protocol_type: ProtocolType
    config: str


@dataclass(frozen=True)
class Region:
    flag: str
    name: str
    code: str


api_type_to_model: dict[ApiType, type[Base_APIConfig]] = {
    ApiType.x_ui: XUI_APIConfig,
    ApiType.mock: Mock_APIConfig,
}
