import asyncio
import logging

from presentation.main import init_api, run_api

logger = logging.getLogger(__name__)


async def app():

    logger.info("Launch bot")
    app = init_api()
    await run_api(app=app)


def main() -> None:
    asyncio.run(app())


if __name__ == "__main__":
    main()