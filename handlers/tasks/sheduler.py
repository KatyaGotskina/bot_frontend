from aiogram import Bot

from core.config import settings
from core.sheduler import scheduler
from core.tg_bot import bot
from utils.request import do_request


async def send_statistic_message(bot: Bot):
    async with do_request(
            url=f'{settings.BOT_BACKEND_HOST}/user/chats',
            method='GET',
            headers={'auth_key': settings.AUTH_KEY},
    ) as response:
        if response.status != 200:
            return
        users_infos = await response.json()
        for user_info in users_infos['items']:
            async with do_request(
                    url=f'{settings.BOT_BACKEND_HOST}/task/all?undone=True',
                    method='GET',
                    headers={'user_from_id': str(user_info['user_id']), 'auth_key': settings.AUTH_KEY}
            ) as tasks_response:
                if tasks_response.status != 200:
                    return
                tasks = await tasks_response.json()
                if not tasks:
                    await bot.send_message(
                        user_info['chat_id'],
                        'Привет,\nВсе твои задачи выполнены! Обязательно возвращайся с новыми задачами завтра!'
                    )
                else:
                    text_base = 'Привет,\nне забудь про выполнение задач:\n'
                    for task in tasks:
                        text_base += f'{task["name"]}\n'
                    await bot.send_message(user_info['chat_id'], text_base)


scheduler.add_job(send_statistic_message, trigger='cron', hour=20, minute=57, kwargs={'bot': bot})

