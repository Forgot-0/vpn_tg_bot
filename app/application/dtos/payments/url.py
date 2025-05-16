from dataclasses import dataclass


@dataclass
class PaymentDTO:
    url: str
    price: float
    discount: int | None = None