import asyncio
import logging

from infrastructure.log.init import configure_logging
from presentation.main import init_api, run_api

logger = logging.getLogger(__name__)


async def app():
    configure_logging()

    logger.info("Launch bot")
    app = init_api()
    await run_api(app=app)


def main() -> None:
    asyncio.run(app())


if __name__ == "__main__":
    main()