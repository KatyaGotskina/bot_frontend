from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot_frontend.core.buttons import get_main_keyboard, START_TASK, during_the_task_keyboard
from bot_frontend.handlers.tasks.router import task_router
from bot_frontend.states.do_tasks import TaskState


@task_router.message(F.text == START_TASK)
async def ask_name(message: types.Message, state: FSMContext):
    await state.set_state(TaskState.enter_task_name)
    await message.answer(
        'Введите название',
        reply_markup=get_main_keyboard(),
    )


@task_router.message(TaskState.enter_task_name)
async def get_name(message: types.Message, state: FSMContext) -> None:
    task_name = message.text
    await message.answer(
        f'засек начало {task_name}',
        reply_markup=during_the_task_keyboard(),
    )

