import base64

from infra.payments.youkass.payment import YouKassaPaymentService
from settings.config import Config


def inti_youkass(config: Config):
    return YouKassaPaymentService(
        base64.b64encode(
            f'{config.yookass.account_id}:{config.yookass.secret_id}'.encode('utf-8')
        ).decode('utf-8')
    )