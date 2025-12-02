from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar, Iterable


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


class ProtocolType(str, Enum):
    VLESS = "vless"
    mock = "MOCK"


@dataclass(frozen=True)
class ProtocolConfig:
    config: dict[str, Any]
    protocol_type: ProtocolType


class ApiType(Enum):
    x_ui = "3X-UI"
    mock = "MOCK"


@dataclass(frozen=True)
class APIConfig:
    ip: str
    panel_port: int
    panel_path: str

    domain: str | None = field(default=None)


@dataclass(frozen=True)
class APICredits:
    username: str
    password: str
    twoFactorCode: str | None = field(default=None)


@dataclass
class VPNConfig:
    protocol_type: ProtocolType
    config: str



@dataclass(frozen=True)
class Region:
    flag: str
    name: str
    code: str

    _REGIONS: ClassVar[dict[str, "Region"]] = {}

    def __str__(self) -> str:
        return f"{self.flag} {self.name} ({self.code})"

    @classmethod
    def register(cls, region: "Region") -> None:
        cls._REGIONS[region.code.upper()] = region

    @classmethod
    def region_by_code(cls, code: str) -> "Region":
        key = code.strip().upper()
        return cls._REGIONS[key]


    @classmethod
    def all_regions(cls) -> Iterable["Region"]:
        return tuple(cls._REGIONS.values())


for r in (
    Region("🇳🇱", "Нидерланды", "NL"),
    Region("🇺🇸", "США", "US"),
    Region("🇬🇧", "Великобритания", "GB"),
):
    Region.register(r)
