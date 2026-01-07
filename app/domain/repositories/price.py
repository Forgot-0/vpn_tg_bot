from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.price import PriceConfig
from app.domain.values.servers import ProtocolType, Region



@dataclass
class BasePriceRepository(ABC):
    @abstractmethod
    async def get_price_config(self) -> PriceConfig: ...

    @abstractmethod
    async def add_region(self, region: Region, coef: float) -> None: ...

    @abstractmethod
    async def add_protocol(self, protocol: ProtocolType, coef: float) -> None: ...

    @abstractmethod
    async def update(self, cfg: PriceConfig) -> None: ...
