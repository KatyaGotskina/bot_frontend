import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bot_api.router import tg_router
from core.tg_bot import bot
from core.webhook import setup_webhook
from core.background_tasks import tg_background_tasks
from middleware.logger import LogServerMiddleware


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # type: ignore
        allow_credentials=True,  # type: ignore
        allow_methods=['*'],  # type: ignore
        allow_headers=['*'],  # type: ignore
    )
    app.add_middleware(LogServerMiddleware)


def setup_routers(app: FastAPI) -> None:
    app.include_router(tg_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print('START APP')
    await setup_webhook(bot)
    yield
    logging.info('Stopping')

    while len(tg_background_tasks) > 0:
        logging.info('%s tasks left', len(tg_background_tasks))
        await asyncio.sleep(0)

    logging.info('Stopped')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app
