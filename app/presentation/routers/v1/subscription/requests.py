from pydantic import BaseModel


class CreateSubscriptionRequests(BaseModel):
    duration: int
    device_count: int
    protocol_types: list[str]

