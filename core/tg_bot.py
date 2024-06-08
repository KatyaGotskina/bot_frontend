import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import F
from aiogram.types import BotCommand

from bot_frontend.core.buttons import *
from bot_frontend.core.config import settings
from bot_frontend.handlers.base_functional.router import base_router
from bot_frontend.handlers.tasks.router import task_router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot=bot)
dp.include_router(task_router)
dp.include_router(base_router)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Start bot')
        ]
    )
    await dp.start_polling(bot)


@dp.message(F.text == 'привет')
async def echo_massage(message: types.Message):
    await message.answer(
        'Привет',
        reply_markup=get_main_keyboard(),
    )


if __name__ == "__main__":
    asyncio.run(main())

