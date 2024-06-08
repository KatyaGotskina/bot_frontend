import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand

from bot_frontend.core.buttons import *
from bot_frontend.core.config import settings
from bot_frontend.handlers.tasks.router import task_router
from bot_frontend.states.do_tasks import TaskState
from bot_frontend.utils.request import do_request

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot=bot)
dp.include_router(task_router)


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


@dp.message(F.text == TO_TASKS)
async def to_tasks(message: types.Message, state: FSMContext):
    await state.set_state(TaskState.task_worker)
    await message.answer(
        text="Поработаем над задачами!",
        reply_markup=during_the_task_keyboard(),
    )


@dp.message(F.text == START_TASK)
async def start_task(message: types.Message, state: FSMContext):
    await state.set_state(TaskState.enter_task_name)
    await message.answer(
        text="Введите название задачи",
        reply_markup=during_the_task_keyboard(),
    )


@dp.message(TaskState.enter_task_name)
async def get_name(message: types.Message, state: FSMContext) -> None:
    task_name = message.text
    response = await do_request(url='http://127.0.0.1:8000/task', params={'name': task_name})
    async with response:
        if response.status == 201:
            await state.set_state(TaskState.task_worker)
            await message.answer(
                f'засек начало "{task_name}"',
                reply_markup=during_the_task_keyboard(),
            )
        elif response.status == 409:
            await state.set_state(TaskState.conflict_task)
            await message.answer(
                f'Задча с таким названием уже существует. Вы точно хотите использовать имя "{task_name}"?',
                reply_markup=yes_no_keyboard(),
            )
        else:
            await message.answer(
                'Произошла ошибка. Введите название повторно',
                reply_markup=during_the_task_keyboard(),
            )

@dp.message(TaskState.conflict_task)
async def work_with_conflict_task(message: types.Message, state: FSMContext) -> None:
    if message.text == "ДА":
        await state.set_state(TaskState.task_worker)
        await message.answer(
            'OK',
            reply_markup=during_the_task_keyboard(),
        )
    else:
        await state.set_state(TaskState.enter_task_name)
        await message.answer(
            'Введите новое имя',
            reply_markup=during_the_task_keyboard(),
        )




if __name__ == "__main__":
    asyncio.run(main())

