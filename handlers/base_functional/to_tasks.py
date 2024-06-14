from aiogram import F, types
from aiogram.fsm.context import FSMContext

from core.buttons import TO_TASKS, during_the_task_keyboard
from handlers.base_functional.router import base_router
from states.do_tasks import TaskState


@base_router.message(F.text == TO_TASKS)
async def to_tasks(message: types.Message, state: FSMContext):
    await state.set_state(TaskState.task_worker)
    await message.answer(
        text="Поработаем над задачами!",
        reply_markup=during_the_task_keyboard(),
    )
