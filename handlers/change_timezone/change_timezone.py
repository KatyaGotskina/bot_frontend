from aiogram import F, types

from core.buttons import timezone_kb, CHANGE_TIME_ZONE, timezone_hours
from core.config import settings
from handlers.change_timezone.router import user_router
from handlers.tasks import task_config
from utils.request import do_request


@user_router.message(F.text == CHANGE_TIME_ZONE)
async def echo_massage(message: types.Message):
    await message.answer(
        'Выберете свой часовой пояс:',
        reply_markup=timezone_kb,
    )


@user_router.callback_query(F.data.in_(timezone_hours))
async def process_buttons_press(callback):
    async with do_request(
            url=f'{settings.BOT_BACKEND_HOST}/user',
            params={'offset': int(callback.data)},
            headers={'user_from_id': str(callback.from_user.id)}
    ) as response:
        if response.status == 200:
            await callback.answer('Часовой пояс сохранен')
        else:
            await callback.answer(task_config.ERROR_MESSAGE)
