from aiogram import types

DISPLAY_STATISTICS = 'вывести статистику'
START_TASK = 'начать дело'
RENAME_TASK = 'переименовать текущее дело'
STOP_TASK = 'завершить дело'


def get_main_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=DISPLAY_STATISTICS)],
        [types.KeyboardButton(text=START_TASK)],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def during_the_task_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=DISPLAY_STATISTICS)],
        [types.KeyboardButton(text=RENAME_TASK)],
        [types.KeyboardButton(text=STOP_TASK)],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
