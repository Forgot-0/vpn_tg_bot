from aiohttp import web

from settings.config import settings



def main():
    app = web.Application()
    web.run_app(app=app, host=settings.webapp.host, port=settings.webapp.port)





main()