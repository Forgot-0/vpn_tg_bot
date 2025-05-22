import logging

from api.main import init_api, run_api
from bot.main import init_webhook
from configs.app import app_settings
from infrastructure.log.init import configure_logging

logger = logging.getLogger(__name__)


def bot_webhook():
    configure_logging()

    logger.info("Launch bot")
    app = init_api()
    init_webhook(app)
    run_api(app=app, host=app_settings.WEBAPP_WEBHOOK_HOST, port=app_settings.WEBAPP_WEBHOOK_PORT)


if __name__ == "__main__":
    bot_webhook()