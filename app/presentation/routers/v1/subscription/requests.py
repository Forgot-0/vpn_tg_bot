from pydantic import BaseModel


class CreateSubscriptionRequests(BaseModel):
    duration_days: int
    device_count: int
    protocol_types: list[str]


class RenewSubscriptionRequests(BaseModel):
    duration_days: int
