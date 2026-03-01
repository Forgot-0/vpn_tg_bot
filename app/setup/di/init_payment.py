import base64

from app.infrastructure.payments.yookassa.apayment import YooKassaPaymentService
from app.configs.app import app_settings


def inti_yookass() -> YooKassaPaymentService:
    return YooKassaPaymentService(
        shop_id=str(app_settings.PAYMENT_ID),
        api_key=app_settings.PAYMENT_SECRET
    )