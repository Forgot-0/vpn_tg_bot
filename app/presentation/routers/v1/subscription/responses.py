from pydantic import BaseModel


class PriceSubscriptionResponse(BaseModel):
    price: float


class PaymentUrlResponse(BaseModel):
    url: str