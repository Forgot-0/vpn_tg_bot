from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.offer import Offer
from app.domain.entities.price import Price
from app.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    async def get_by_code(self, code: str) -> Product | None: ...

    @abstractmethod
    async def add(self, product: Product) -> None: ...

    @abstractmethod
    async def update(self, product: Product) -> None: ...


class PriceRepository(ABC):
    @abstractmethod
    async def get_by_id(self, price_id: UUID) -> Price | None: ...

    @abstractmethod
    async def list_active_by_plan(self, plan_id: UUID) -> list[Price]: ...

    @abstractmethod
    async def add(self, price: Price) -> None: ...

    @abstractmethod
    async def update(self, price: Price) -> None: ...


class OfferRepository(ABC):
    @abstractmethod
    async def get_by_id(self, offer_id: UUID) -> Offer | None: ...

    @abstractmethod
    async def list_active(self) -> list[Offer]: ...

    @abstractmethod
    async def list_by_plan(self, plan_id: UUID) -> list[Offer]: ...

    @abstractmethod
    async def add(self, offer: Offer) -> None: ...

    @abstractmethod
    async def update(self, offer: Offer) -> None: ...
