from aiogram import types


START_TASK = 'начать дело'
RENAME_TASK = 'переименовать текущее дело'
STOP_TASK = 'завершить дело'
GO_BACK = "вернуться"

TO_TASKS = "К делам"
STATISTICS = "Статистика"
CHANGE_TIME_ZONE = "Изменить часовой пояс"


def get_main_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=TO_TASKS)],
        [types.KeyboardButton(text=STATISTICS)],
        [types.KeyboardButton(text=CHANGE_TIME_ZONE)],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def during_the_task_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=START_TASK)],
        [types.KeyboardButton(text=RENAME_TASK)],
        [types.KeyboardButton(text=STOP_TASK)],
        [types.KeyboardButton(text=GO_BACK)],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def yes_no_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="ДА")],
        [types.KeyboardButton(text="НЕТ")],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)