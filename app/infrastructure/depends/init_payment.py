import base64

from infrastructure.payments.yookassa.apayment import YooKassaPaymentService
from configs.app import settings


def inti_yookass():
    return YooKassaPaymentService(
        base64.b64encode(
            f'{settings.PAYMENT_ID}:{settings.PAYMENT_SECRET}'.encode('utf-8')
        ).decode('utf-8')
    )