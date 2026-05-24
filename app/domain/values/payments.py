from enum import StrEnum


class PaymentStatus(StrEnum):
    PENDING = "pending"
    WAITING_FOR_CAPTURE = "waiting_for_capture"
    SUCCEEDED = "succeeded"
    CANCELLED = "cancelled"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProvider(StrEnum):
    YOOKASSA = "yookassa"
    STRIPE = "stripe"
    CRYPTO = "crypto"
    OTHER = "other"
