from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot_frontend.core.buttons import START_TASK, during_the_task_keyboard, yes_no_keyboard, go_back_keyboard, GO_BACK
from bot_frontend.core.config import settings
from bot_frontend.handlers.tasks import task_config
from bot_frontend.handlers.tasks.router import task_router
from bot_frontend.states.do_tasks import TaskState
from bot_frontend.utils.request import do_request


@task_router.message(F.text == START_TASK)
async def start_task(message: types.Message, state: FSMContext):
    await state.set_state(TaskState.enter_task_name)
    await message.answer(
        text="Введите название задачи",
        reply_markup=go_back_keyboard(),
    )


@task_router.message(TaskState.enter_task_name)
async def get_name(message: types.Message, state: FSMContext) -> None:
    task_name = message.text
    if task_name == GO_BACK:
        await state.set_state(TaskState.task_worker)
        await message.answer(text=task_config.BACK_TO_TASKS_MENU, reply_markup=during_the_task_keyboard())
        return
    async with do_request(url=f'{settings.BOT_BACKEND_HOST}/task', params={'name': task_name}) as response:
        if response.status == 201:
            await state.set_state(TaskState.task_worker)
            await message.answer(f'засек начало "{task_name}"', reply_markup=during_the_task_keyboard())
        elif response.status == 409:
            await state.set_state(TaskState.conflict_task)
            await state.set_data({f'{message.chat.id}_old_task_name': task_name})
            await message.answer(
                f'Задача с таким названием уже существует. Вы точно хотите использовать имя "{task_name}"?',
                reply_markup=yes_no_keyboard(),
            )
        else:
            await message.answer(task_config.ERROR_MESSAGE, reply_markup=during_the_task_keyboard())


@task_router.message(TaskState.conflict_task)
async def work_with_conflict_task(message: types.Message, state: FSMContext) -> None:
    if message.text == "ДА":
        task_name = (await state.get_data()).get(f'{message.chat.id}_old_task_name')
        async with do_request(
            url=f'{settings.BOT_BACKEND_HOST}/task',
            params={'name': task_name, 'forcibly': True}
        ) as response:
            if response.status == 201:
                await state.set_state(TaskState.task_worker)
                await message.answer('OK', reply_markup=during_the_task_keyboard())
            else:
                await message.answer(task_config.ERROR_MESSAGE, reply_markup=during_the_task_keyboard())
    else:
        await state.set_state(TaskState.enter_task_name)
        await message.answer('Введите новое имя', reply_markup=during_the_task_keyboard())
