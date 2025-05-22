import logging
from aiohttp import web

from api.paid import router as paid_router


logger = logging.getLogger(__name__)


def init_api():
    app = web.Application()
    app.add_routes(routes=paid_router)
    return app

def run_api(app: web.Application, host: str, port: int):
    logger.info("Running app")
    web.run_app(app, host=host, port=port)