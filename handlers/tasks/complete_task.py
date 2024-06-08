from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot_frontend.core.buttons import during_the_task_keyboard, STOP_TASK, get_tasks_keyboard, FORWARD, GO_BACK
from bot_frontend.handlers.tasks.router import task_router
from bot_frontend.states.do_tasks import TaskState
from bot_frontend.utils.request import do_request


@task_router.message(F.text == STOP_TASK)
async def complete_task(message: types.Message, state: FSMContext) -> None:
    await state.set_state(TaskState.complete_task)
    response = await do_request(url='http://127.0.0.1:8000/task/all?undone=True', method='GET')

    message_text = "Выберете задачу, которую хотите завершить, и напишите ее номер: \n\n"
    counter = 1
    state_data = await state.get_data()

    async with response:
        if response.status == 200:
            if not await response.json():
                await message.answer('Текущих задач нет', reply_markup=during_the_task_keyboard())
                return
            for task in await response.json():
                task_start = task['start'].split('T')[0] + " " + task['start'].split('T')[1][:-7]
                message_text += f"""{counter}. "{task['name']}"\n Время начала: {task_start}\n\n"""
                state_data[f"{message.chat.id}_task_{counter}"] =  task['id']
                counter += 1
            state_data[f"{message.chat.id}_max_counter"] = counter
            await state.set_data(state_data)
            message_text += "..."
            await message.answer(message_text, reply_markup=get_tasks_keyboard())
        else:
            await message.answer('Произошла ошибка. Введите название повторно', reply_markup=during_the_task_keyboard())


@task_router.message(TaskState.complete_task)
async def get_and_complete_task(message: types.Message, state: FSMContext) -> None:
    if message.text and message.text not in ["вернуться", "Листать задачи дальше"]:
        task_id = (await state.get_data()).get(f"{message.chat.id}_task_{message.text}")
        if task_id:
            response = await do_request(url=f'http://127.0.0.1:8000/task/{task_id}', method='DELETE')
            async with response:
                if response.status == 204:
                    await message.answer('Дело завершено', reply_markup=get_tasks_keyboard())
                    return
                await message.answer('Произошла ошибка. Повторите попытку', reply_markup=get_tasks_keyboard())
                return
        await message.answer('Введите корректное число', reply_markup=get_tasks_keyboard())

    elif message.text == FORWARD:

        message_text = "Выберете задачу, которую хотите завершить, и напишите ее номер: \n\n"
        state_data = await state.get_data()
        max_counter = (await state.get_data()).get(f"{message.chat.id}_max_counter")

        response = await do_request(
            url=f'http://127.0.0.1:8000/task/all?offset={max_counter}&undone=True',
            method='GET'
        )
        if not await response.json():
            await message.answer(
                'Больше задач нет',
                reply_markup=during_the_task_keyboard(),
            )
            return
        for task in await response.json():
            task_start = task['start'].split('T')[0] + " " + task['start'].split('T')[1][:-7]
            message_text += f"""{max_counter}. "{task['name']}"\n Время начала: {task_start}\n\n"""
            state_data[f"{message.chat.id}_task_{max_counter}"] = task['id']
            max_counter += 1
        state_data[f"{message.chat.id}_max_counter"] = max_counter
        await state.set_data(state_data)
        message_text += "..."
        await message.answer(message_text, reply_markup=get_tasks_keyboard())

    elif message.text == GO_BACK:
        await state.set_state(TaskState.task_worker)
        await message.answer('Вернулись в меню задач', reply_markup=during_the_task_keyboard())
