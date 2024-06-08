from aiogram import F, types
from aiogram.fsm.context import FSMContext

from bot_frontend.core.buttons import GO_BACK
from bot_frontend.handlers.base_functional.router import base_router
from bot_frontend.states.utils import state_to_keyboard, state_to_massage, previous_states


@base_router.message(F.text == GO_BACK)
async def go_back(message: types.Message, state: FSMContext):
    previous_state = previous_states[await state.get_state()]
    await state.set_state(previous_state)
    await message.answer(
        text=state_to_massage[previous_state],
        reply_markup=state_to_keyboard[previous_state],
    )
