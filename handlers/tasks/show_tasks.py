from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot_frontend.core.buttons import during_the_task_keyboard, get_tasks_keyboard, FORWARD, GO_BACK, STATISTICS
from bot_frontend.core.config import settings
from bot_frontend.handlers.tasks import task_config
from bot_frontend.handlers.tasks.general import make_message_and_get_data
from bot_frontend.handlers.tasks.router import task_router
from bot_frontend.states.do_tasks import TaskState
from bot_frontend.utils.request import do_request


@task_router.message(F.text == STATISTICS)
async def show_tasks(message: types.Message, state: FSMContext) -> None:
    await state.set_state(TaskState.show_tasks)

    async with do_request(url=f'{settings.BOT_BACKEND_HOST}/task/all', method='GET') as response:
        if response.status == 200:
            tasks = await response.json()
            if not tasks:
                await message.answer('У Вас еще нет дел!', reply_markup=during_the_task_keyboard())
                return
            message_text, data_for_state, _ = await make_message_and_get_data(
                tasks,
                1,
                message.chat.id,
                add_task_end=True
            )
            data_for_state[f"{message.chat.id}_max_counter"] = 5
            await state.set_data(data_for_state)
            await message.answer(message_text, reply_markup=get_tasks_keyboard())
        else:
            await message.answer(task_config.ERROR_MESSAGE, reply_markup=during_the_task_keyboard())


@task_router.message(TaskState.show_tasks)
async def get_and_show_tasks(message: types.Message, state: FSMContext) -> None:
    if message.text == FORWARD:

        max_counter = (await state.get_data()).get(f"{message.chat.id}_max_counter")

        async with do_request(
            url=f'{settings.BOT_BACKEND_HOST}/task/all?offset={max_counter}',
            method='GET'
        ) as response:
            tasks = await response.json()
            if not tasks:
                await message.answer('Больше задач нет', _markup=during_the_task_keyboard())
                return
            message_text, data_for_state, max_counter = await make_message_and_get_data(
                tasks,
                max_counter,
                message.chat.id,
                add_task_end=True
            )
            data_for_state[f"{message.chat.id}_max_counter"] = max_counter
            await state.set_data(data_for_state)
            await message.answer(message_text, reply_markup=get_tasks_keyboard())

    elif message.text == GO_BACK:
        await state.set_state(TaskState.task_worker)
        await message.answer(task_config.BACK_TO_TASKS_MENU, reply_markup=during_the_task_keyboard())
