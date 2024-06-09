from typing import Any


async def make_message_and_get_data(
        tasks: list[dict[str, Any]],
        max_counter: int,
        chat_id: int,
        add_task_end: bool = False,
) -> tuple[str, dict[str, int], int]:
    message_text = "" if add_task_end else "Выберете задачу, которую хотите завершить, и напишите ее номер: \n\n"
    data_for_state = {}

    for task in tasks:
        task_start = await get_str_time(task['start'])
        task_end = await get_str_time(task['end']) if task['end'] else "Еще не завершено"
        if not add_task_end:
            message_text += f"""{max_counter}. "{task['name']}"\n Время начала: {task_start}\n\n"""
        else:
            message_text += f"""{max_counter}. "{task['name']}"\n Время начала: {task_start}\n Время конца: {task_end}\n\n"""
        data_for_state[f"{chat_id}_task_{max_counter}"] = task['id']
        max_counter += 1
    message_text += "..."

    return message_text, data_for_state, max_counter


async def get_str_time(task_time: str) -> str:
    return task_time.split('T')[0] + " " + task_time.split('T')[1][:-7]
