import base64

from infrastructure.payments.yookassa.apayment import YooKassaPaymentService
from settings.config import Config


def inti_yookass(config: Config):
    return YooKassaPaymentService(
        base64.b64encode(
            f'{config.yookass.account_id}:{config.yookass.secret_id}'.encode('utf-8')
        ).decode('utf-8')
    )