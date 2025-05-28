import logging

from api.main import init_api
from bot.main import init_webhook
from configs.app import app_settings
from infrastructure.log.init import configure_logging

logger = logging.getLogger(__name__)


async def app():
    configure_logging()

    logger.info("Launch bot")
    app = init_api()
    init_webhook(app)
    return app
