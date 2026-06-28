from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    WAITING_PAYMENT = "WAITING_PAYMENT"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
