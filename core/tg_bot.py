import asyncio
import logging

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram.types import BotCommand

from core.buttons import *
from core.config import settings
from core.sheduler import scheduler
from handlers.base_functional.router import base_router
from handlers.change_timezone.router import user_router
from handlers.tasks.router import task_router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot=bot)


def get_dispatcher() -> Dispatcher:
    global dp

    return dp


def get_tg_bot() -> Bot:
    global bot

    return bot


async def main():
    dp.include_router(task_router)
    dp.include_router(base_router)
    dp.include_router(user_router)

    await bot.delete_webhook()

    logging.basicConfig(level=logging.DEBUG)
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Start bot')
        ]
    )
    await dp.start_polling(bot)


@dp.message(F.text == '/start')
async def echo_massage(message: types.Message):
    await message.answer(
        'Привет!',
        reply_markup=get_main_keyboard(),
    )


async def start_scheduler():
    scheduler.start()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(main())
    loop.create_task(start_scheduler())
    loop.run_forever()
