import base64

from infrastructure.payments.yookassa.apayment import YooKassaPaymentService
from configs.app import app_settings


def inti_yookass():
    return YooKassaPaymentService(
        base64.b64encode(
            f'{app_settings.PAYMENT_ID}:{app_settings.PAYMENT_SECRET}'.encode('utf-8')
        ).decode('utf-8')
    )