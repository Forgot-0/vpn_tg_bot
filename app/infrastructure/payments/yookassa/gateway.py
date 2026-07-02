from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

import httpx

from app.application.dtos.payments import GatewayPaymentResult, GatewayStatusResult
from app.application.interfaces.payments import PaymentGateway
from app.configs.app import app_config
from app.domain.entities.payment import Payment
from app.domain.values.payments import PaymentProvider, PaymentStatus


_YOOKASSA_STATUS_MAP: dict[str, PaymentStatus] = {
    "pending": PaymentStatus.PENDING,
    "waiting_for_capture": PaymentStatus.WAITING_FOR_CAPTURE,
    "succeeded": PaymentStatus.SUCCEEDED,
    "canceled": PaymentStatus.CANCELLED,
}


@dataclass
class YooKassaPaymentGateway(PaymentGateway):
    api_base: str = "https://api.yookassa.ru/v3"
    timeout: float = 30.0

    @property
    def provider(self) -> PaymentProvider:
        return PaymentProvider.YOOKASSA

