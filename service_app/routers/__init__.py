import logging
from starlette.types import ASGIApp

from service_app.routers.router import router as main_router


class RouterRegister:
    routers = [main_router]

    @classmethod
    def register(cls, app: ASGIApp):
        logging.info("Adding routers")
        for app_router in cls.routers:
            try:
                app.include_router(app_router)
            except Exception as e:
                logging.exception("Unable to register router")
                raise e
