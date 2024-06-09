from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot_frontend.core.buttons import during_the_task_keyboard, STOP_TASK, get_tasks_keyboard, FORWARD, GO_BACK
from bot_frontend.core.config import settings
from bot_frontend.handlers.tasks.general import make_message_and_get_data
from bot_frontend.handlers.tasks.router import task_router
from bot_frontend.handlers.tasks import task_config
from bot_frontend.states.do_tasks import TaskState
from bot_frontend.utils.request import do_request


@task_router.message(F.text == STOP_TASK)
async def complete_task(message: types.Message, state: FSMContext) -> None:
    await state.set_state(TaskState.complete_task)

    async with do_request(url=f'{settings.BOT_BACKEND_HOST}/task/all?undone=True', method='GET') as response:
        if response.status == 200:
            tasks = await response.json()
            if not tasks:
                await state.set_state(TaskState.task_worker)
                await message.answer('Текущих задач нет', reply_markup=during_the_task_keyboard())
                return
            message_text, data_for_state, _ = await make_message_and_get_data(tasks, 1, message.chat.id)
            data_for_state[f"{message.chat.id}_max_counter"] = 5
            await state.set_data(data_for_state)
            await message.answer(message_text, reply_markup=get_tasks_keyboard())
        else:
            await message.answer(task_config.ERROR_MESSAGE, reply_markup=during_the_task_keyboard())


@task_router.message(TaskState.complete_task)
async def get_and_complete_task(message: types.Message, state: FSMContext) -> None:
    if message.text and message.text not in ["вернуться", "Листать задачи дальше"]:
        task_id = (await state.get_data()).get(f"{message.chat.id}_task_{message.text}")
        if task_id:
            async with do_request(
                url=f'{settings.BOT_BACKEND_HOST}/task/end',
                method='PATCH',
                params={'id': task_id}
            ) as response:
                if response.status == 200:
                    await message.answer('Дело завершено', reply_markup=get_tasks_keyboard())
                    return
                await message.answer(task_config.ERROR_MESSAGE, reply_markup=get_tasks_keyboard())
                return
        await message.answer('Введите корректное число', reply_markup=get_tasks_keyboard())

    elif message.text == FORWARD:
        max_counter = (await state.get_data()).get(f"{message.chat.id}_max_counter")

        async with do_request(
            url=f'{settings.BOT_BACKEND_HOST}/task/all?offset={max_counter}&undone=True',
            method='GET'
        ) as response:
            tasks = await response.json()
            if not tasks:
                await message.answer('Больше задач нет', reply_markup=during_the_task_keyboard())
                return
            message_text, data_for_state, max_counter = await make_message_and_get_data(
                tasks,
                max_counter,
                message.chat.id
            )
            data_for_state[f"{message.chat.id}_max_counter"] = max_counter
            await state.set_data(data_for_state)
            await message.answer(message_text, reply_markup=get_tasks_keyboard())

    elif message.text == GO_BACK:
        await state.set_state(TaskState.task_worker)
        await message.answer(task_config.BACK_TO_TASKS_MENU, reply_markup=during_the_task_keyboard())
