from aiohttp import web
from handlers import create
from handlers import remove


def setup_app(app):
    app.router.add_get("/create/{vpn_client}", create)
    app.router.add_get("/remove/{vpn_client}", remove)

app = web.Application()

if __name__ == "__main__":
    setup_app(app)
    web.run_app(app)