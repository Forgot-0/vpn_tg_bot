from pydantic import BaseModel


class PriceSubscriptionResponse(BaseModel):
    price: float
