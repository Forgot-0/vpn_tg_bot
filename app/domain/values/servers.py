from dataclasses import dataclass, field
from enum import StrEnum


class PanelType(StrEnum):
    X3UI = "3x-ui"
    REMNAWAVE = "remnawave"
    OTHER = "other"


@dataclass(frozen=True)
class PanelCredits:
    username: str
    password: str
    two_factor_code: str | None = field(default=None)

@dataclass
class PanelConfig:
    ip: str
    panel_port: int
    panel_path: str

    domain: str | None = field(default=None)

    def set_domain(self, domain: str) -> None:
        self.domain = domain
