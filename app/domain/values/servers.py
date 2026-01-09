from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar, Iterable
from urllib.parse import urlparse


class ProtocolType(str, Enum):
    VLESS = "vless"
    TROJAN = "trojan"
    SS = "shadowsocks"


@dataclass(frozen=True)
class ProtocolConfig:
    config: dict[str, Any]
    protocol_type: ProtocolType


@dataclass(frozen=True)
class SubscriptionConfig:
    domain: str
    port: int
    path: str
    url: str

    @classmethod
    def from_url(cls, url: str) -> "SubscriptionConfig":
        if url[-1] != "/":
            url += "/"

        parsed_url = urlparse(url)
        domain = parsed_url.hostname
        if domain is None:
            raise

        port = parsed_url.port if parsed_url.port else 443
        path = parsed_url.path
        return SubscriptionConfig(domain=domain, port=port, path=path, url=url)



class ApiType(Enum):
    x_ui = "3X-UI"


@dataclass
class APIConfig:
    ip: str
    panel_port: int
    panel_path: str

    domain: str | None = field(default=None)

    def set_domain(self, domain: str) -> None:
        self.domain = domain


@dataclass(frozen=True)
class APICredits:
    username: str
    password: str
    twoFactorCode: str | None = field(default=None)


@dataclass
class VPNConfig:
    config: str
    protocol_type: ProtocolType | None = field(default=None)


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
        if key not in cls._REGIONS:
            raise

        return cls._REGIONS[key]


    @classmethod
    def all_regions(cls) -> Iterable["Region"]:
        return tuple(cls._REGIONS.values())


for r in (
    Region("🇳🇱", "Нидерланды", "NL"),
    Region("🇺🇸", "США", "US"),
    Region("🇬🇧", "Великобритания", "GB"),
    Region("🇩🇪", "Германия", "DE"),
    Region("🇮🇹", "Италия", "IT"),
    Region("🇫🇷", "Франция", "FR"),
    Region("🇯🇵", "Япония", "JP"),
    Region("🇰🇷", "Южная Корея", "KR"),
    Region("🇨🇦", "Канада", "CA"),
    Region("🇮🇳", "Индия", "IN"),
    Region("🇨🇭", "Швейцария", "CH"),
    Region("🇦🇺", "Австралия", "AU"),
    Region("🇪🇸", "Испания", "ES"),
    Region("🇧🇷", "Бразилия", "BR"),
    Region("🇷🇺", "Россия", "RU"),
    Region("🇮🇱", "Израиль", "IL"),
    Region("🇸🇪", "Швеция", "SE"),
    Region("🇳🇿", "Новая Зеландия", "NZ"),
    Region("🇲🇽", "Мексика", "MX"),
):
    Region.register(r)
