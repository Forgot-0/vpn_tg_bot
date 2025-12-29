from dataclasses import dataclass


@dataclass
class PaymentData:
    url: str
    price: float
    discount: int | None = None